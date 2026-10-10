package org.slaviccases.app

import android.content.Context
import org.json.JSONObject

data class Choice(val key: String, val text: String)
data class Question(
    val id: String, val caseId: String, val track: String,
    val nativeText: Map<String, String>, val instruction: Map<String, String>,
    val prompt: String, val choices: List<Choice>, val correctKey: String, val draft: Boolean
)
data class CaseInfo(val id: String, val name: String)
data class LanguagePack(val code: String, val name: String, val cases: List<CaseInfo>, val questions: List<Question>)

object Lessons {
    fun load(context: Context): List<LanguagePack> {
        val root = JSONObject(context.assets.open("content.json").bufferedReader().use { it.readText() })
        require(root.getInt("schema_version") == 1)
        val languages = root.getJSONArray("languages")
        return (0 until languages.length()).map { index ->
            val language = languages.getJSONObject(index)
            val cases = language.getJSONArray("cases")
            val samples = language.getJSONArray("samples")
            val questions = mutableListOf<Question>()
            for (s in 0 until samples.length()) {
                val sample = samples.getJSONObject(s)
                val draft = sample.getString("review_status") != "reviewed"
                if (draft && !BuildConfig.DEBUG) continue
                val sentences = sample.getJSONArray("sentences")
                for (q in 0 until sentences.length()) {
                    val item = sentences.getJSONObject(q)
                    val options = item.getJSONObject("options")
                    questions += Question(item.getString("id"), sample.getString("case"), sample.getString("track"),
                        item.getJSONObject("native_text").strings(), sample.getJSONObject("instruction").strings(),
                        item.getString("neutral_prompt"), listOf("a", "b", "c", "d").map { Choice(it, options.getString(it)) },
                        item.getString("correct"), draft)
                }
            }
            LanguagePack(language.getString("learning_language"), language.getString("name"),
                (0 until cases.length()).map { CaseInfo(cases.getJSONObject(it).getString("id"), cases.getJSONObject(it).getString("name")) }, questions)
        }
    }
    private fun JSONObject.strings(): Map<String, String> = keys().asSequence().associateWith { getString(it) }
}
