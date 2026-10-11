package org.slaviccases.app

import androidx.compose.ui.test.*
import androidx.compose.ui.test.junit4.createAndroidComposeRule
import org.junit.Rule
import org.junit.Test

class PracticeFlowTest {
    @get:Rule val app = createAndroidComposeRule<MainActivity>()

    @Test fun germanFourCasesAndTranslationDoNotRevealAnswer() {
        try {
            app.onNodeWithText("Settings").performScrollTo().performClick()
            app.onNodeWithText("German simple").performScrollTo().performClick()
            app.onNodeWithText("Deutsch").performScrollTo().performClick()
            app.onNodeWithText("Zurück").performScrollTo().performClick()
            app.onNodeWithText("Nominativ · Nominativ").assertExists()
            app.onNodeWithText("Genitiv · Genitiv").assertExists()
            app.onNodeWithText("Akkusativ · Akkusativ").assertExists()
            app.onNodeWithText("Dativ · Dativ").performScrollTo().performClick()
            app.onNodeWithText("Substantive · 15").performClick()
            app.onNodeWithText("Ich helfe dem Mann.").assertDoesNotExist()
            app.onNodeWithText("dem Mann").performScrollTo().performClick()
            app.onNodeWithText("Richtig!").assertExists()
        } finally {
            app.activity.getSharedPreferences("settings", 0).edit()
                .putString("gui", "en").putString("learning", "ru").commit()
        }
    }

    @Test fun topicGenderNavigationAndThemePersist() {
        try {
            app.onNodeWithText("Settings").performScrollTo().performClick()
            app.onNodeWithText("Russian deep").performScrollTo().performClick()
            app.onNodeWithText("Back").performScrollTo().performClick()
            app.onNodeWithText("Nominative · Именительный").performScrollTo().performClick()
            app.onNodeWithText("Nouns · 91").performClick()
            app.onNodeWithText("Genders · 35").performScrollTo().performClick()
            app.onNodeWithText("Feminine · 12").performScrollTo().performClick()
            app.onNodeWithText("1 / 12 · Nominative").assertExists()
            val button = if (app.onAllNodesWithText("Dark").fetchSemanticsNodes().isNotEmpty()) "Dark" else "Light"
            app.onNodeWithText(button).performClick()
            app.activityRule.scenario.recreate()
            app.onNodeWithText(if (button == "Dark") "Light" else "Dark").assertExists()
            app.onNodeWithText("1 / 12 · Nominative").assertExists()
            app.onNodeWithText("Back").performScrollTo().performClick()
            app.onNodeWithText("All genders · 35").assertExists()
        } finally {
            app.activity.getSharedPreferences("settings", 0).edit()
                .putString("learning", "ru").remove("theme").commit()
        }
    }

    @Test fun nounSessionSurvivesRecreationAndRepeats() {
        app.onNodeWithText("Dative · Дательный").performScrollTo().performClick()
        app.onNodeWithText("Nouns · 15").performClick()
        app.onNodeWithText("Speak").assertIsNotEnabled()
        val questions = Lessons.load(app.activity).first { it.id == "ru" }.questions
            .filter { it.caseId == "dative" && it.track == "nouns" }
        questions.forEachIndexed { index, question ->
            app.onNodeWithText(question.choices.first { it.key == question.correctKey }.text).performScrollTo().performClick()
            app.onNodeWithText("Correct!").performScrollTo().assertIsDisplayed()
            if (index == 0) {
                app.onNodeWithText("Speak").assertIsEnabled().performClick()
                app.activityRule.scenario.recreate()
                app.onNodeWithText("Correct!").performScrollTo().assertIsDisplayed()
                app.onNodeWithText("Next").assertIsEnabled()
            }
            app.onNodeWithText("Next").performClick()
        }
        app.onNodeWithText("15 / 15").assertIsDisplayed()
        app.onNodeWithText("Repeat").performClick()
        app.onNodeWithText("1 / 15 · Dative").assertIsDisplayed()
        app.onNodeWithText("Next").assertIsNotEnabled()
    }

    @Test fun wrongAnswerLocksAndMixedReturnsToMainMenu() {
        app.onNodeWithText("Mixed practice · 15 questions").performScrollTo().performClick()
        val prompt = Lessons.load(app.activity).first { it.id == "ru" }.questions
            .first { question -> app.onAllNodesWithText(question.prompt).fetchSemanticsNodes().isNotEmpty() }
        val wrong = prompt.choices.first { it.key != prompt.correctKey }
        app.onNodeWithText(wrong.text).performScrollTo().performClick()
        app.onNodeWithText("Incorrect. The correct answer is highlighted.").assertExists()
        app.onNodeWithText(wrong.text + " — Incorrect").assertIsNotEnabled()
        app.onNodeWithText("Back").performScrollTo().performClick()
        app.onNodeWithText("Choose a case").assertExists()
    }

    @Test fun interfaceAndLearningLanguagesAreIndependentAndPersist() {
        try {
            app.onNodeWithText("Settings").performScrollTo().performClick()
            app.onNodeWithText("Deutsch").performClick()
            app.onAllNodesWithText("Russisch einfach").filter(isSelected()).assertCountEquals(1)
            app.onNodeWithText("Polnisch einfach").performClick()
            app.activityRule.scenario.recreate()
            app.onNodeWithText("Sprache der Oberfläche").assertExists()
            app.onNodeWithText("Grammatische Fälle lernen").assertExists()
            app.onAllNodesWithText("Polnisch einfach").filter(isSelected()).assertCountEquals(1)
            app.onNodeWithText("Zurück").performClick()
            app.onNodeWithText("Vokativ · Wołacz").assertExists()
            app.onNodeWithText("Dativ · Celownik").performScrollTo().performClick()
            app.onNodeWithText("Adjektive und Zahlwörter · 15").performClick()
            val first = Lessons.load(app.activity).first { it.id == "pl" }.questions
                .first { it.caseId == "dative" && it.track == "adjectives" }
            app.onNodeWithText(first.nativeText.getValue("de")).assertExists()
            app.onNodeWithText(first.prompt).assertExists()
        } finally {
            // Tests share one installed app, so leave the next launch at defaults.
            app.activity.getSharedPreferences("settings", 0).edit()
                .putString("gui", "en").putString("learning", "ru").commit()
        }
    }
}
