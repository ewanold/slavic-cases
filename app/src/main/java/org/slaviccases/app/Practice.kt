package org.slaviccases.app

import kotlin.random.Random

/** Pure session rules, shared by the UI and JVM regression tests. */
object Practice {
    fun <T> mixed(items: List<T>, seed: Int, size: Int = 15): List<T> = items.shuffled(Random(seed)).take(size)
    fun <T> options(items: List<T>, questionId: String, seed: Int): List<T> =
        items.shuffled(Random(seed xor questionId.hashCode()))
    fun score(correctKeys: List<String>, answers: List<String>): Int =
        correctKeys.zip(answers).count { (correct, answer) -> correct == answer }
}
