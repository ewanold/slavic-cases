package org.slaviccases.app

import android.content.res.Configuration
import android.os.Bundle
import android.os.Build
import android.speech.tts.TextToSpeech
import androidx.activity.ComponentActivity
import androidx.activity.compose.BackHandler
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.background
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.saveable.listSaver
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalConfiguration
import androidx.compose.ui.unit.dp
import java.util.Locale
import kotlin.random.Random
import kotlinx.coroutines.delay

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            val prefs = remember { getSharedPreferences("settings", 0) }
            var theme by rememberSaveable { mutableStateOf(prefs.getString("theme", "system") ?: "system") }
            val dark = if (theme == "system") isSystemInDarkTheme() else theme == "dark"
            val colors = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
                if (dark) dynamicDarkColorScheme(this) else dynamicLightColorScheme(this)
            } else if (dark) {
                darkColorScheme(primary = Color(0xFFA1CBE5), secondary = Color(0xFFBCCC9E))
            } else {
                lightColorScheme(primary = Color(0xFF355F78), secondary = Color(0xFF586B42))
            }
            MaterialTheme(colorScheme = colors) {
                SlavicApp(dark) { theme = if (dark) "light" else "dark"; prefs.edit().putString("theme", theme).apply() }
            }
        }
    }
}

/** Resolves UI resources using the chosen GUI locale, independent of the phone. */
private class Labels(private val context: android.content.Context) {
    fun text(@androidx.annotation.StringRes id: Int, vararg args: Any): String = context.getString(id, *args)
    fun case(id: String): String = when (id) {
        "nominative" -> text(R.string.case_nominative)
        "genitive" -> text(R.string.case_genitive)
        "dative" -> text(R.string.case_dative)
        "accusative" -> text(R.string.case_accusative)
        "instrumental" -> text(R.string.case_instrumental)
        "prepositional" -> text(R.string.case_prepositional)
        "locative" -> text(R.string.case_locative)
        "vocative" -> text(R.string.case_vocative)
        else -> id
    }
    fun gender(id: String): String = when (id) {
        "feminine" -> text(R.string.gender_feminine)
        "masculine" -> text(R.string.gender_masculine)
        "neuter" -> text(R.string.gender_neuter)
        else -> id
    }
}

private val stringListSaver = listSaver<List<String>, String>(save = { it }, restore = { it.toList() })

@Composable
private fun SlavicApp(dark: Boolean, toggleTheme: () -> Unit) {
    val context = LocalContext.current
    val prefs = remember { context.getSharedPreferences("settings", 0) }
    var gui by rememberSaveable { mutableStateOf(prefs.getString("gui", "en") ?: "en") }
    val deviceConfiguration = LocalConfiguration.current
    val labels = remember(context, gui, deviceConfiguration) {
        val configuration = Configuration(deviceConfiguration).apply {
            setLocale(Locale.forLanguageTag(gui))
        }
        Labels(context.createConfigurationContext(configuration))
    }
    val loaded = remember { runCatching { Lessons.load(context) } }
    val packs = loaded.getOrNull()
    if (packs.isNullOrEmpty()) {
        Surface(Modifier.fillMaxSize()) {
            Column(Modifier.safeDrawingPadding().padding(24.dp)) {
                Text(labels.text(R.string.app_name), style = MaterialTheme.typography.headlineLarge)
                Text(labels.text(R.string.content_load_error))
            }
        }
        return
    }
    var learning by rememberSaveable { mutableStateOf(prefs.getString("learning", "ru") ?: "ru") }
    var autoContinue by rememberSaveable { mutableStateOf(prefs.getBoolean("autoContinue", false)) }
    var guessCount by rememberSaveable { mutableIntStateOf(prefs.getInt("guessCount", 30).coerceIn(1, 200)) }
    var guessMode by rememberSaveable { mutableStateOf(false) }
    var pauseAutoContinue by rememberSaveable { mutableStateOf(false) }
    val pack = packs.firstOrNull { it.id == learning } ?: packs.first()
    var route by rememberSaveable { mutableStateOf("menu") }
    var selectedTrack by rememberSaveable { mutableStateOf("") }
    var selectedTopic by rememberSaveable { mutableStateOf("") }
    var selectedGender by rememberSaveable { mutableStateOf("") }
    var selectedCase by rememberSaveable { mutableStateOf("") }
    var questionIds by rememberSaveable(stateSaver = stringListSaver) { mutableStateOf(emptyList<String>()) }
    var answers by rememberSaveable(stateSaver = stringListSaver) { mutableStateOf(emptyList<String>()) }
    var position by rememberSaveable { mutableIntStateOf(0) }
    var sessionSeed by rememberSaveable { mutableIntStateOf(0) }
    var origin by rememberSaveable { mutableStateOf("menu") }
    var speechMessage by remember { mutableStateOf("") }
    val speechSnackbar = remember { SnackbarHostState() }
    var speechReady by remember { mutableStateOf(false) }
    var engine by remember { mutableStateOf<TextToSpeech?>(null) }
    DisposableEffect(context) {
        val tts = TextToSpeech(context) { status -> speechReady = status == TextToSpeech.SUCCESS }
        engine = tts
        onDispose { tts.stop(); tts.shutdown(); engine = null }
    }
    LaunchedEffect(gui, learning) { prefs.edit().putString("gui", gui).putString("learning", learning).apply() }
    LaunchedEffect(guessCount) { prefs.edit().putInt("guessCount", guessCount).apply() }
    LaunchedEffect(autoContinue) { prefs.edit().putBoolean("autoContinue", autoContinue).apply() }
    LaunchedEffect(speechMessage) {
        if (speechMessage.isNotEmpty()) speechSnackbar.showSnackbar(speechMessage)
    }
    val session = questionIds.mapNotNull { id -> pack.questions.firstOrNull { it.id == id } }
        .map { if (guessMode) Practice.guessCase(it, pack.cases) else it }
    fun start(questions: List<Question>, from: String, guessing: Boolean = false) {
        if (questions.isEmpty()) return
        guessMode = guessing
        questionIds = questions.map { it.id }; answers = emptyList()
        pauseAutoContinue = false
        position = 0; sessionSeed = Random.nextInt(); origin = from; speechMessage = ""; route = "question"
    }
    fun back() {
        engine?.stop(); speechMessage = ""
        route = when (route) { "question", "results" -> origin; "genders" -> "topics"; "topics" -> "tracks"; "tracks", "settings" -> "menu"; else -> "menu" }
    }
    fun next() {
        engine?.stop(); speechMessage = ""; pauseAutoContinue = false
        if (position + 1 < session.size) position++ else route = "results"
    }
    LaunchedEffect(autoContinue, pauseAutoContinue, route, position, answers, questionIds, sessionSeed) {
        if (autoContinue && !pauseAutoContinue && route == "question" &&
            position < session.size && answers.getOrNull(position) != null) {
            delay(2_000)
            next()
        }
    }
    BackHandler(enabled = route != "menu") { back() }
    Scaffold(
        topBar = {
            Column(Modifier.fillMaxWidth().statusBarsPadding().padding(horizontal = 20.dp, vertical = 12.dp)) {
                Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                    Text(labels.text(R.string.app_name), modifier = Modifier.weight(1f), style = MaterialTheme.typography.headlineSmall)
                    TextButton(onClick = toggleTheme) { Text(labels.text(if (dark) R.string.theme_light else R.string.theme_dark)) }
                }
                Text(pack.displayName(gui), style = MaterialTheme.typography.labelLarge)
            }
        },
        bottomBar = {
            if (route == "question" && position < session.size) {
                val question = session[position]
                val selected = answers.getOrNull(position)
                Column(Modifier.fillMaxWidth().navigationBarsPadding().padding(16.dp)) {
                    if (selected != null) Text(
                        if (selected == question.correctKey) labels.text(R.string.feedback_correct)
                        else labels.text(R.string.feedback_incorrect),
                        modifier = Modifier.padding(bottom = 8.dp)
                    )
                Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                    OutlinedButton(enabled = selected != null, onClick = {
                        pauseAutoContinue = true
                        val tts = engine
                        val locale = Locale.forLanguageTag(pack.code)
                        if (tts == null || !speechReady || tts.isLanguageAvailable(locale) < TextToSpeech.LANG_AVAILABLE) {
                            speechMessage = labels.text(R.string.speech_no_voice)
                        } else {
                            val languageStatus = tts.setLanguage(locale)
                            val voice = tts.voices?.firstOrNull {
                                !it.isNetworkConnectionRequired && it.locale.language == locale.language &&
                                    !it.features.contains(TextToSpeech.Engine.KEY_FEATURE_NOT_INSTALLED)
                            }
                            if (languageStatus < TextToSpeech.LANG_AVAILABLE || voice == null) {
                                speechMessage = labels.text(R.string.speech_no_offline_voice)
                            } else {
                                tts.voice = voice
                                val status = tts.speak(if (guessMode) pack.questions.first { it.id == question.id }.let { original -> original.choices.first { it.key == original.correctKey }.text } else question.choices.first { it.key == selected }.text, TextToSpeech.QUEUE_FLUSH, null, question.id)
                                speechMessage = if (status == TextToSpeech.ERROR) labels.text(R.string.speech_unavailable) else ""
                            }
                        }
                    }) { Text(labels.text(R.string.speak)) }
                    Button(enabled = selected != null, onClick = { next() }) { Text(labels.text(R.string.next)) }
                }
                }
            }
        },
        snackbarHost = { SnackbarHost(speechSnackbar) }
    ) { padding ->
        Column(Modifier.fillMaxSize().padding(padding).verticalScroll(rememberScrollState())
            .padding(horizontal = 20.dp, vertical = if (route == "question") 8.dp else 20.dp),
            verticalArrangement = Arrangement.spacedBy(if (route == "question") 8.dp else 12.dp)) {
            if (route != "menu") TextButton(onClick = { back() }) { Text(labels.text(R.string.back)) }
            when (route) {
                "menu" -> {
                    Text(labels.text(R.string.choose_case), style = MaterialTheme.typography.titleLarge)
                    if (pack.questions.any { it.draft }) {
                        Text(labels.text(R.string.draft_notice),
                            color = MaterialTheme.colorScheme.secondary)
                    }
                    pack.cases.forEach { case ->
                        OutlinedButton(modifier = Modifier.fillMaxWidth(), enabled = pack.questions.any { it.caseId == case.id }, onClick = {
                            selectedCase = case.id; route = "tracks"
                        }) { Text(labels.text(R.string.case_with_native_name, labels.case(case.id), case.name)) }
                    }
                    Button(modifier = Modifier.fillMaxWidth(), enabled = pack.questions.isNotEmpty(), onClick = {
                        start(Practice.mixed(pack.questions, Random.nextInt()), "menu")
                    }) { Text(labels.text(R.string.mixed_practice)) }
                    Button(modifier = Modifier.fillMaxWidth(), enabled = pack.questions.isNotEmpty(), onClick = {
                        start(Practice.mixed(pack.questions, Random.nextInt(), guessCount), "menu", guessing = true)
                    }) { Text(labels.text(R.string.label_with_count, labels.text(R.string.guess_case), minOf(guessCount, pack.questions.size))) }
                    TextButton(onClick = { route = "settings" }) { Text(labels.text(R.string.settings)) }
                }
                "tracks" -> {
                    Text(labels.case(selectedCase), style = MaterialTheme.typography.headlineSmall)
                    listOf("nouns", "adjectives").forEach { track ->
                        val questions = pack.questions.filter { it.caseId == selectedCase && it.track == track }
                        OutlinedButton(modifier = Modifier.fillMaxWidth(), enabled = questions.isNotEmpty(), onClick = {
                            selectedTrack = track
                            if (questions.any { it.topicId.isNotEmpty() }) route = "topics" else start(questions, "tracks")
                        }) {
                            Text(labels.text(R.string.label_with_count, labels.text(if (track == "nouns") R.string.nouns else R.string.adjectives_numerals), questions.size))
                        }
                    }
                }
                "topics" -> {
                    Text(labels.case(selectedCase), style = MaterialTheme.typography.headlineSmall)
                    pack.questions.filter { it.caseId == selectedCase && it.track == selectedTrack }
                        .groupBy { it.topicId }.forEach { (topic, questions) ->
                            OutlinedButton(modifier = Modifier.fillMaxWidth(), onClick = {
                                selectedTopic = topic
                                if (questions.any { it.gender.isNotEmpty() }) route = "genders" else start(questions, "topics")
                            }) { Text(labels.text(R.string.label_with_count, questions.first().topicLabel(gui), questions.size)) }
                        }
                }
                "genders" -> {
                    val questions = pack.questions.filter { it.caseId == selectedCase && it.track == selectedTrack && it.topicId == selectedTopic }
                    Text(questions.firstOrNull()?.topicLabel(gui) ?: "", style = MaterialTheme.typography.headlineSmall)
                    OutlinedButton(modifier = Modifier.fillMaxWidth(), onClick = { selectedGender = ""; start(questions, "genders") }) {
                        Text(labels.text(R.string.label_with_count, labels.text(R.string.all_genders), questions.size))
                    }
                    questions.groupBy { it.gender }.forEach { (gender, items) ->
                        OutlinedButton(modifier = Modifier.fillMaxWidth(), onClick = { selectedGender = gender; start(items, "genders") }) {
                            Text(labels.text(R.string.label_with_count, labels.gender(gender), items.size))
                        }
                    }
                }
                "settings" -> {
                    Text(labels.text(R.string.interface_language), style = MaterialTheme.typography.titleLarge)
                    listOf(
                        "en" to R.string.language_english, "de" to R.string.language_german,
                        "ru" to R.string.language_russian, "pl" to R.string.language_polish
                    ).chunked(2).forEach { languages ->
                        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                            languages.forEach { (code, name) ->
                                FilterChip(selected = gui == code, onClick = { gui = code }, label = { Text(labels.text(name)) })
                            }
                        }
                    }
                    Text(labels.text(R.string.learning_language), style = MaterialTheme.typography.titleLarge)
                    packs.forEach { language ->
                        FilterChip(selected = pack.id == language.id, onClick = { learning = language.id }, label = { Text(language.displayName(gui)) })
                    }
                    Text(labels.text(R.string.translation_policy))
                    Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = androidx.compose.ui.Alignment.CenterVertically) {
                        Text(labels.text(R.string.auto_continue), modifier = Modifier.weight(1f))
                        Switch(checked = autoContinue, onCheckedChange = { autoContinue = it })
                    }
                    Text(labels.text(R.string.auto_continue_description))
                    Text(labels.text(R.string.guess_count),
                        style = MaterialTheme.typography.titleMedium)
                    Row(verticalAlignment = androidx.compose.ui.Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                        OutlinedButton(enabled = guessCount > 1, onClick = { guessCount-- }) { Text(labels.text(R.string.decrease)) }
                        Text(labels.text(R.string.count_value, guessCount))
                        OutlinedButton(enabled = guessCount < 200, onClick = { guessCount++ }) { Text(labels.text(R.string.increase)) }
                    }
                    Text(labels.text(R.string.version_value, BuildConfig.VERSION_NAME))
                    Text(labels.text(R.string.build_date_value, BuildConfig.BUILD_DATE))
                }
                "question" -> {
                    val question = session.getOrNull(position)
                    if (question == null) {
                        Text(labels.text(R.string.session_unavailable))
                    } else {
                        val selected = answers.getOrNull(position)
                        Text(labels.text(R.string.question_progress, position + 1, session.size, if (guessMode) labels.text(R.string.guess_case) else labels.case(question.caseId)), style = MaterialTheme.typography.titleMedium)
                        LinearProgressIndicator(progress = { position.toFloat() / session.size }, modifier = Modifier.fillMaxWidth())
                        Text(if (guessMode) labels.text(R.string.guess_case_instruction) else question.instruction[gui] ?: labels.text(R.string.translation_missing), style = MaterialTheme.typography.bodyMedium)
                        Card(Modifier.fillMaxWidth()) {
                            Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
                                if (gui != pack.code) Text(question.nativeText[gui] ?: labels.text(R.string.sentence_translation_missing))
                                Text(question.prompt, style = MaterialTheme.typography.headlineSmall)
                            }
                        }
                        Practice.options(question.choices, question.id, sessionSeed).forEach { choice ->
                            val isCorrect = selected != null && choice.key == question.correctKey
                            val isWrong = selected == choice.key && !isCorrect
                            val background = when {
                                isCorrect -> if (dark) Color(0xFF17452A) else Color(0xFFD9EFDE)
                                isWrong -> if (dark) Color(0xFF632824) else Color(0xFFFADBD8)
                                else -> MaterialTheme.colorScheme.surface
                            }
                            val foreground = when {
                                isCorrect -> if (dark) Color(0xFFB7F0C7) else Color(0xFF14532D)
                                isWrong -> if (dark) Color(0xFFFFDAD6) else Color(0xFF8B1D18)
                                else -> MaterialTheme.colorScheme.onSurface
                            }
                            val choiceLabel = if (guessMode) labels.text(R.string.case_with_native_name, labels.case(choice.key), choice.text) else choice.text
                            val answerLabel = when {
                                isCorrect -> labels.text(R.string.answer_correct, choiceLabel)
                                isWrong -> labels.text(R.string.answer_incorrect, choiceLabel)
                                else -> choiceLabel
                            }
                            OutlinedButton(modifier = Modifier.fillMaxWidth(), enabled = selected == null,
                                colors = ButtonDefaults.outlinedButtonColors(containerColor = background, contentColor = foreground,
                                    disabledContainerColor = background, disabledContentColor = foreground),
                                onClick = { if (answers.size == position) answers = answers + choice.key }) {
                                Text(answerLabel, style = MaterialTheme.typography.titleMedium)
                            }
                        }
                    }
                }
                "results" -> {
                    val correct = Practice.score(session.map { it.correctKey }, answers)
                    Text(labels.text(R.string.practice_complete), style = MaterialTheme.typography.headlineMedium)
                    Text(labels.text(R.string.score_value, correct, session.size), style = MaterialTheme.typography.displayMedium)
                    Text(labels.text(R.string.score_percent, if (session.isEmpty()) 0 else correct * 100 / session.size))
                    Button(modifier = Modifier.fillMaxWidth(), onClick = { start(session, origin, guessing = guessMode) }) { Text(labels.text(R.string.repeat)) }
                    OutlinedButton(modifier = Modifier.fillMaxWidth(), onClick = { back() }) { Text(labels.text(R.string.back_to_menu)) }
                }
            }
        }
    }
}
