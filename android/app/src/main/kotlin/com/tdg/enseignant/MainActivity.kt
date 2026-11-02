package com.tdg.enseignant

import android.app.Activity
import android.content.Intent
import android.net.Uri
import android.util.AtomicFile
import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel
import java.io.File
import java.io.ByteArrayOutputStream

class MainActivity : FlutterActivity() {
    private var dictionaryEngine: DictionaryEngine? = null
    private var pending: MethodChannel.Result? = null
    private var backup: String? = null
    private val dataFile get() = AtomicFile(File(filesDir, "enseignant_v1.json"))
    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)
        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, "com.tdg.enseignant/storage")
            .setMethodCallHandler { call, result ->
                try {
                    when(call.method) {
                        "dictionaryInfo", "dictionarySearch", "dictionaryEntry" -> {
                            val engine = dictionaryEngine ?: DictionaryEngine(this).also { dictionaryEngine = it }
                            engine.handle(call, result)
                        }
                        "read" -> result.success(if (dataFile.baseFile.exists()) dataFile.openRead().bufferedReader().use { it.readText() } else null)
                        "write" -> {
                            val bytes = (call.arguments as String).toByteArray(Charsets.UTF_8)
                            val stream = dataFile.startWrite()
                            try { stream.write(bytes); dataFile.finishWrite(stream) }
                            catch(e: Exception) { dataFile.failWrite(stream); throw e }
                            result.success(null)
                        }
                        "export" -> {
                            if(pending != null) { result.error("busy", "Une opération est déjà ouverte", null); return@setMethodCallHandler }
                            pending = result; backup = call.arguments as String
                            try {
                                startActivityForResult(Intent(Intent.ACTION_CREATE_DOCUMENT).apply {
                                    addCategory(Intent.CATEGORY_OPENABLE); type = "application/json"
                                    putExtra(Intent.EXTRA_TITLE, "Enseignant-sauvegarde.json")
                                }, 501)
                            } catch(e: Exception) { pending = null; backup = null; throw e }
                        }
                        "import" -> {
                            if(pending != null) { result.error("busy", "Une opération est déjà ouverte", null); return@setMethodCallHandler }
                            pending = result
                            try {
                                startActivityForResult(Intent(Intent.ACTION_OPEN_DOCUMENT).apply {
                                    addCategory(Intent.CATEGORY_OPENABLE); type = "*/*"
                                }, 502)
                            } catch(e: Exception) { pending = null; throw e }
                        }
                        "openUrl" -> {
                            val uri = Uri.parse(call.arguments as String)
                            if(uri.scheme !in listOf("https", "mailto", "tel")) throw IllegalArgumentException("Lien non accepté")
                            startActivity(Intent(Intent.ACTION_VIEW, uri)); result.success(null)
                        }
                        else -> result.notImplemented()
                    }
                } catch(e: Exception) { result.error("storage", e.localizedMessage, null) }
            }
    }
    override fun onDestroy() {
        dictionaryEngine?.close()
        dictionaryEngine = null
        super.onDestroy()
    }
    @Deprecated("Android activity result compatibility")
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if(requestCode != 501 && requestCode != 502) return
        val result = pending ?: return
        pending = null
        try {
            val uri = data?.data
            if(resultCode != Activity.RESULT_OK || uri == null) { result.success(null); return }
            if(requestCode == 501) {
                val stream = contentResolver.openOutputStream(uri, "wt") ?: throw IllegalStateException("Fichier inaccessible")
                stream.use { it.write((backup ?: throw IllegalStateException("Sauvegarde absente")).toByteArray(Charsets.UTF_8)) }
                result.success(true)
            } else {
                val stream = contentResolver.openInputStream(uri) ?: throw IllegalStateException("Fichier inaccessible")
                val bytes = stream.use { input ->
                    val out = ByteArrayOutputStream()
                    val buffer = ByteArray(8192)
                    while(true) {
                        val count = input.read(buffer)
                        if(count < 0) break
                        out.write(buffer, 0, count)
                        if(out.size() > 10 * 1024 * 1024) throw IllegalArgumentException("Sauvegarde trop volumineuse")
                    }
                    out.toByteArray()
                }
                if(bytes.size > 10 * 1024 * 1024) throw IllegalArgumentException("Sauvegarde trop volumineuse (10 Mo maximum)")
                result.success(String(bytes, Charsets.UTF_8))
            }
        } catch(e: Exception) { result.error("document", e.localizedMessage, null) }
        finally { backup = null }
    }
}
