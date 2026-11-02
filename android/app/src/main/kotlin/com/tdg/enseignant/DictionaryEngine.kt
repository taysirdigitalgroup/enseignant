package com.tdg.enseignant

import android.content.Context
import android.database.Cursor
import android.database.sqlite.SQLiteDatabase
import android.os.Handler
import android.os.Looper
import io.flutter.FlutterInjector
import io.flutter.plugin.common.MethodCall
import io.flutter.plugin.common.MethodChannel
import java.io.ByteArrayInputStream
import java.util.zip.InflaterInputStream
import java.io.File
import org.json.JSONObject
import java.text.Normalizer
import java.util.Locale
import java.util.concurrent.Executors

/** La base lexicale reste hors du thread d'interface. */
class DictionaryEngine(private val context: Context) {
    private val worker = Executors.newSingleThreadExecutor()
    private val main = Handler(Looper.getMainLooper())
    private var database: SQLiteDatabase? = null

    private fun assetFile(asset: String, cacheName: String): File {
        val destination = File(context.cacheDir, cacheName)
        if (!destination.exists()) {
            val temporary = File(context.cacheDir, "$cacheName.part")
            val key = FlutterInjector.instance().flutterLoader().getLookupKeyForAsset(asset)
            context.assets.open(key).use { input -> temporary.outputStream().use { input.copyTo(it) } }
            if (!temporary.renameTo(destination)) {
                temporary.delete()
                throw IllegalStateException("Impossible de préparer la référence hors connexion")
            }
        }
        return destination
    }
    private fun db(): SQLiteDatabase {
        database?.let { return it }
        val file = assetFile("assets/dictionary/modern.sqlite", "modern_v210.sqlite")
        return SQLiteDatabase.openDatabase(file.absolutePath, null, SQLiteDatabase.OPEN_READONLY).also { database = it }
    }
    private fun normalize(value: String): String {
        val expanded = value.lowercase(Locale.ROOT).replace("œ", "oe").replace("æ", "ae")
            .replace('’', '\'').replace('−', '-').replace('–', '-')
        return Normalizer.normalize(expanded, Normalizer.Form.NFD)
            .replace(Regex("\\p{M}+"), "").replace(Regex("\\s+"), " ").trim()
    }
    private fun summary(cursor: Cursor): Map<String, Any?> = mapOf(
        "id" to cursor.getLong(0), "headword" to cursor.getString(1),
        "letter" to cursor.getString(2), "category" to cursor.getString(3),
        "startPage" to cursor.getInt(4), "endPage" to cursor.getInt(5),
        "preview" to cursor.getString(6), "source" to cursor.getString(7)
    )
    private fun search(call: MethodCall): Map<String, Any> {
        val query = normalize((call.argument<String>("query") ?: "").take(200))
        val mode = call.argument<String>("mode") ?: "word"
        val letter = call.argument<String>("letter") ?: ""
        val category = call.argument<String>("category") ?: ""
        val offset = (call.argument<Number>("offset")?.toInt() ?: 0).coerceAtLeast(0)
        val limit = (call.argument<Number>("limit")?.toInt() ?: 60).coerceIn(1, 100)
        val ids = call.argument<List<Number>>("ids")
        val source = call.argument<String>("source") ?: ""
        val conditions = mutableListOf<String>()
        val arguments = mutableListOf<String>()
        if (source.isNotEmpty()) { conditions.add("source = ?"); arguments.add(source) }
        if (letter.isNotEmpty()) { conditions.add("letter = ?"); arguments.add(letter) }
        if (category.isNotEmpty()) { conditions.add("(category = ? OR (source='Wiktionnaire' AND instr(' / ' || category || ' / ', ' / ' || ? || ' / ')>0) OR (source='FranceTerme' AND category LIKE ?))"); arguments.add(category); arguments.add(category); arguments.add("$category / %") }
        if (ids != null) {
            val clean = ids.map { it.toLong() }.filter { it > 0 }.distinct()
            // Les entiers du codec sont contrôlés avant interpolation ; aucune chaîne SQL utilisateur.
            conditions.add(if (clean.isEmpty()) "0" else "id IN (${clean.joinToString(",")})")
        }
        if (query.isNotEmpty()) {
            when (mode) {
                "exact" -> { conditions.add("id IN (SELECT entry_id FROM aliases WHERE alias=?)"); arguments.add(query) }
                "definitions" -> {
                    val tokens = Regex("[\\p{L}\\p{N}]+").findAll(query).map { it.value }.take(12).toList()
                    if (tokens.isEmpty()) conditions.add("0") else {
                        conditions.add("id IN (SELECT docid FROM dictionary_fts WHERE dictionary_fts MATCH ?)")
                        val match = tokens.joinToString(" AND ") { "$it*" }; arguments.add(match)
                    }
                }
                else -> { conditions.add("id IN (SELECT entry_id FROM aliases WHERE alias >= ? AND alias < ?)"); arguments.add(query); arguments.add(query + '\uffff') }
            }
        }
        val clause = if (conditions.isEmpty()) "1" else conditions.joinToString(" AND ")
        val args = arguments.toTypedArray()
        val total = db().rawQuery("SELECT count(*) FROM entries WHERE $clause", args).use { it.moveToFirst(); it.getInt(0) }
        val rows = mutableListOf<Map<String, Any?>>()
        db().rawQuery("SELECT id,headword,letter,category,start_page,end_page,preview,source FROM entries WHERE $clause ORDER BY CASE WHEN normalized=? THEN 0 ELSE 1 END, CASE source WHEN 'Wiktionnaire' THEN 0 WHEN 'FranceTerme' THEN 1 ELSE 2 END, CASE WHEN letter='#' THEN 1 ELSE 0 END,normalized,id LIMIT $limit OFFSET $offset", args + arrayOf(query)).use { cursor ->
            while (cursor.moveToNext()) rows.add(summary(cursor))
        }
        return mapOf("rows" to rows, "total" to total, "offset" to offset, "hasMore" to (offset + rows.size < total))
    }
    private fun entry(id: Long): Map<String, Any?> {
        db().rawQuery("SELECT id,headword,letter,category,start_page,end_page,preview,source,paragraphs,body,refs,y,source_url,licence,publication FROM entries WHERE id=?", arrayOf(id.toString())).use { cursor ->
            if (!cursor.moveToFirst()) throw IllegalArgumentException("Article introuvable")
            return summary(cursor) + mapOf(
                "paragraphs" to InflaterInputStream(ByteArrayInputStream(cursor.getBlob(8))).bufferedReader(Charsets.UTF_8).use { it.readText() }, "body" to InflaterInputStream(ByteArrayInputStream(cursor.getBlob(9))).bufferedReader(Charsets.UTF_8).use { it.readText() },
                "references" to cursor.getString(10), "y" to cursor.getDouble(11),
                "sourceUrl" to cursor.getString(12), "licence" to cursor.getString(13), "publication" to cursor.getString(14),
                "alternatives" to alternatives(cursor.getString(1), id)
            )
        }
    }
    private fun alternatives(word: String, id: Long): List<Map<String, Any?>> {
        val rows = mutableListOf<Map<String, Any?>>()
        db().rawQuery("SELECT id,headword,letter,category,start_page,end_page,preview,source FROM entries WHERE normalized=? AND id<>? ORDER BY CASE source WHEN 'Wiktionnaire' THEN 0 WHEN 'FranceTerme' THEN 1 ELSE 2 END", arrayOf(normalize(word), id.toString())).use { cursor ->
            while (cursor.moveToNext()) {
                if (cursor.getString(1).lowercase(Locale.ROOT) == word.lowercase(Locale.ROOT)) rows.add(summary(cursor))
            }
        }
        return rows
    }
    private fun info(): String {
        return db().rawQuery("SELECT value FROM metadata WHERE key='modern'", null).use { it.moveToFirst(); JSONObject(it.getString(0)).toString() }
    }
    fun handle(call: MethodCall, result: MethodChannel.Result) {
        worker.execute {
            try {
                val value: Any? = when (call.method) {
                    "dictionaryInfo" -> info()
                    "dictionarySearch" -> search(call)
                    "dictionaryEntry" -> entry(call.argument<Number>("id")?.toLong() ?: 0L)
                    else -> throw IllegalArgumentException("Opération de dictionnaire inconnue")
                }
                main.post { result.success(value) }
            } catch (error: Exception) {
                main.post { result.error("dictionary", error.localizedMessage ?: "Référence indisponible", null) }
            }
        }
    }
    fun close() {
        worker.execute { database?.close(); database = null }
        worker.shutdown()
    }
}
