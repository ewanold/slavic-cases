package org.slaviccases.app

import org.junit.Assert.*
import org.junit.Test

class PracticeTest {
    @Test fun mixedIsFiniteWithoutReplacement() {
        val session = Practice.mixed((0..179).toList(), 42)
        assertEquals(15, session.size)
        assertEquals(15, session.toSet().size)
        assertEquals(session, Practice.mixed((0..179).toList(), 42))
        assertEquals(3, Practice.mixed(listOf(1, 2, 3), 42).size)
    }
    @Test fun guessCaseUsesCompletedFormAndCaseIdentity() {
        val original = Question("q", "accusative", "nouns", mapOf("en" to "I see a friend."), emptyMap(),
            "Я вижу ___. (друг)", listOf(Choice("a", "друг"), Choice("b", "друга")), "b", true)
        val cases = listOf(CaseInfo("nominative", "Именительный"), CaseInfo("accusative", "Винительный"))
        val question = Practice.guessCase(original, cases)
        assertEquals("accusative", question.correctKey)
        assertEquals(listOf("nominative", "accusative"), question.choices.map { it.key })
        assertTrue(question.prompt.contains("Я вижу друга."))
        assertFalse(question.prompt.contains("___"))
        assertEquals(original.nativeText, question.nativeText)
    }
    @Test fun configuredSessionSizeIsBoundedByAvailableQuestions() {
        assertEquals(30, Practice.mixed((1..100).toList(), 42, 30).size)
        assertEquals(7, Practice.mixed((1..7).toList(), 42, 30).toSet().size)
    }
    @Test fun optionShufflePreservesIdentityAndStaysStable() {
        val choices = listOf("a", "b", "c", "d")
        val shuffled = Practice.options(choices, "ru-dative-01", 9)
        assertEquals(choices.toSet(), shuffled.toSet())
        assertEquals(shuffled, Practice.options(choices, "ru-dative-01", 9))
    }
    @Test fun scoreCountsAnsweredQuestionsOnly() {
        assertEquals(1, Practice.score(listOf("a", "b", "c"), listOf("a", "d")))
        assertEquals(0, Practice.score(listOf("a"), emptyList()))
    }
}
