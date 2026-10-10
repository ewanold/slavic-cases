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
