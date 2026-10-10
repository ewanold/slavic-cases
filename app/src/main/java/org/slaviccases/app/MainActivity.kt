package org.slaviccases.app

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
import androidx.compose.ui.unit.dp
import java.util.Locale
import kotlin.random.Random

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            val dark = isSystemInDarkTheme()
            val colors = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
                if (dark) dynamicDarkColorScheme(this) else dynamicLightColorScheme(this)
            } else if (dark) {
                darkColorScheme(primary = Color(0xFFA1CBE5), secondary = Color(0xFFBCCC9E))
            } else {
                lightColorScheme(primary = Color(0xFF355F78), secondary = Color(0xFF586B42))
            }
            MaterialTheme(colorScheme = colors) {
                SlavicApp()
            }
        }
    }
}

private class Labels(private val de: Boolean) {
    fun text(en: String, german: String) = if (de) german else en
    fun case(id: String) = if (de) when (id) {
        "nominative" -> "Nominativ"; "genitive" -> "Genitiv"; "dative" -> "Dativ"
        "accusative" -> "Akkusativ"; "instrumental" -> "Instrumental"
        "prepositional" -> "Präpositiv"; "locative" -> "Lokativ"; "vocative" -> "Vokativ"
        else -> id
    } else id.replaceFirstChar { it.uppercase() }
}

private val stringListSaver = listSaver<List<String>, String>(save = { it }, restore = { it.toList() })

@Composable
private fun SlavicApp() {
    val dark = isSystemInDarkTheme()
    val context = LocalContext.current
    val prefs = remember { context.getSharedPreferences("settings", 0) }
    val loaded = remember { runCatching { Lessons.load(context) } }
    val packs = loaded.getOrNull()
    if (packs.isNullOrEmpty()) {
        Surface(Modifier.fillMaxSize()) {
            Column(Modifier.safeDrawingPadding().padding(24.dp)) {
                Text("Slavic Cases", style = MaterialTheme.typography.headlineLarge)
                Text("Learning material could not be loaded. / Lernmaterial konnte nicht geladen werden.")
            }
        }
        return
    }
    var gui by rememberSaveable { mutableStateOf(prefs.getString("gui", "en") ?: "en") }
    var learning by rememberSaveable { mutableStateOf(prefs.getString("learning", "ru") ?: "ru") }
    val pack = packs.firstOrNull { it.code == learning } ?: packs.first()
    val labels = Labels(gui == "de")
    var route by rememberSaveable { mutableStateOf("menu") }
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
    LaunchedEffect(speechMessage) {
        if (speechMessage.isNotEmpty()) speechSnackbar.showSnackbar(speechMessage)
    }
    val session = questionIds.mapNotNull { id -> pack.questions.firstOrNull { it.id == id } }
    fun start(questions: List<Question>, from: String) {
        if (questions.isEmpty()) return
        questionIds = questions.map { it.id }; answers = emptyList()
        position = 0; sessionSeed = Random.nextInt(); origin = from; speechMessage = ""; route = "question"
    }
    fun back() {
        engine?.stop(); speechMessage = ""
        route = when (route) { "question", "results" -> origin; "tracks", "settings" -> "menu"; else -> "menu" }
    }
    BackHandler(enabled = route != "menu") { back() }
    Scaffold(
        topBar = {
            Column(Modifier.fillMaxWidth().statusBarsPadding().padding(horizontal = 20.dp, vertical = 12.dp)) {
                Text("Slavic Cases", style = MaterialTheme.typography.headlineMedium)
                Text(pack.name, style = MaterialTheme.typography.labelLarge)
            }
        },
        bottomBar = {
            if (route == "question" && position < session.size) {
                val question = session[position]
                val selected = answers.getOrNull(position)
                Row(Modifier.fillMaxWidth().navigationBarsPadding().padding(16.dp), horizontalArrangement = Arrangement.SpaceBetween) {
                    OutlinedButton(enabled = selected != null, onClick = {
                        val tts = engine
                        val locale = Locale.forLanguageTag(pack.code)
                        if (tts == null || !speechReady || tts.isLanguageAvailable(locale) < TextToSpeech.LANG_AVAILABLE) {
                            speechMessage = labels.text("No voice available for this language. Practice can continue.", "Keine Stimme für diese Sprache verfügbar. Du kannst weiter üben.")
                        } else {
                            val languageStatus = tts.setLanguage(locale)
                            val voice = tts.voices?.firstOrNull {
                                !it.isNetworkConnectionRequired && it.locale.language == locale.language &&
                                    !it.features.contains(TextToSpeech.Engine.KEY_FEATURE_NOT_INSTALLED)
                            }
                            if (languageStatus < TextToSpeech.LANG_AVAILABLE || voice == null) {
                                speechMessage = labels.text("No offline voice installed for this language.", "Keine Offline-Stimme für diese Sprache installiert.")
                            } else {
                                tts.voice = voice
                                val status = tts.speak(question.choices.first { it.key == selected }.text, TextToSpeech.QUEUE_FLUSH, null, question.id)
                                speechMessage = if (status == TextToSpeech.ERROR) labels.text("Speech is unavailable.", "Sprachausgabe ist nicht verfügbar.") else ""
                            }
                        }
                    }) { Text(labels.text("Speak", "Vorlesen")) }
                    Button(enabled = selected != null, onClick = {
                        engine?.stop(); speechMessage = ""
                        if (position + 1 < session.size) position++ else route = "results"
                    }) { Text(labels.text("Next", "Weiter")) }
                }
            }
        },
        snackbarHost = { SnackbarHost(speechSnackbar) }
    ) { padding ->
        Column(Modifier.fillMaxSize().padding(padding).verticalScroll(rememberScrollState())
            .padding(horizontal = 20.dp, vertical = if (route == "question") 8.dp else 20.dp),
            verticalArrangement = Arrangement.spacedBy(if (route == "question") 8.dp else 12.dp)) {
            if (route != "menu") TextButton(onClick = { back() }) { Text(labels.text("Back", "Zurück")) }
            when (route) {
                "menu" -> {
                    Text(labels.text("Choose a case", "Wähle einen Fall"), style = MaterialTheme.typography.titleLarge)
                    if (pack.questions.any { it.draft }) {
                        Text(labels.text("Preview lessons · linguistic review pending", "Lektionsvorschau · sprachliche Prüfung ausstehend"),
                            color = MaterialTheme.colorScheme.secondary)
                    }
                    pack.cases.forEach { case ->
                        OutlinedButton(modifier = Modifier.fillMaxWidth(), enabled = pack.questions.any { it.caseId == case.id }, onClick = {
                            selectedCase = case.id; route = "tracks"
                        }) { Text("${labels.case(case.id)} · ${case.name}") }
                    }
                    Button(modifier = Modifier.fillMaxWidth(), enabled = pack.questions.isNotEmpty(), onClick = {
                        start(Practice.mixed(pack.questions, Random.nextInt()), "menu")
                    }) { Text(labels.text("Mixed practice · 15 questions", "Gemischt üben · 15 Fragen")) }
                    TextButton(onClick = { route = "settings" }) { Text(labels.text("Settings", "Einstellungen")) }
                }
                "tracks" -> {
                    Text(labels.case(selectedCase), style = MaterialTheme.typography.headlineSmall)
                    listOf("nouns", "adjectives").forEach { track ->
                        val questions = pack.questions.filter { it.caseId == selectedCase && it.track == track }
                        OutlinedButton(modifier = Modifier.fillMaxWidth(), enabled = questions.isNotEmpty(), onClick = { start(questions, "tracks") }) {
                            Text((if (track == "nouns") labels.text("Nouns", "Substantive") else labels.text("Adjectives and numerals", "Adjektive und Zahlwörter")) + " · ${questions.size}")
                        }
                    }
                }
                "settings" -> {
                    Text(labels.text("Interface language", "Sprache der Oberfläche"), style = MaterialTheme.typography.titleLarge)
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        listOf("en" to "English", "de" to "Deutsch").forEach { (code, name) ->
                            FilterChip(selected = gui == code, onClick = { gui = code }, label = { Text(name) })
                        }
                    }
                    Text(labels.text("Language to learn", "Lernsprache"), style = MaterialTheme.typography.titleLarge)
                    packs.forEach { language ->
                        FilterChip(selected = pack.code == language.code, onClick = { learning = language.code }, label = { Text(language.name) })
                    }
                    Text(labels.text("Sentence translations follow the interface language.", "Satzübersetzungen folgen der Sprache der Oberfläche."))
                    Text("${labels.text("Version", "Version")} ${BuildConfig.VERSION_NAME}")
                    Text("${labels.text("Build date", "Build-Datum")} ${BuildConfig.BUILD_DATE} (UTC)")
                }
                "question" -> {
                    val question = session.getOrNull(position)
                    if (question == null) {
                        Text(labels.text("Session unavailable. Return to the menu.", "Übung nicht verfügbar. Zurück zum Menü."))
                    } else {
                        val selected = answers.getOrNull(position)
                        Text("${position + 1} / ${session.size} · ${labels.case(question.caseId)}", style = MaterialTheme.typography.titleMedium)
                        LinearProgressIndicator(progress = { position.toFloat() / session.size }, modifier = Modifier.fillMaxWidth())
                        Text(question.instruction[gui] ?: labels.text("Translation missing", "Übersetzung fehlt"), style = MaterialTheme.typography.bodyMedium)
                        Card(Modifier.fillMaxWidth()) {
                            Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
                                Text(question.nativeText[gui] ?: labels.text("Translation missing for this language.", "Übersetzung für diese Sprache fehlt."))
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
                            val suffix = when { isCorrect -> labels.text(" — Correct", " — Richtig"); isWrong -> labels.text(" — Incorrect", " — Falsch"); else -> "" }
                            OutlinedButton(modifier = Modifier.fillMaxWidth(), enabled = selected == null,
                                colors = ButtonDefaults.outlinedButtonColors(containerColor = background, contentColor = foreground,
                                    disabledContainerColor = background, disabledContentColor = foreground),
                                onClick = { if (answers.size == position) answers = answers + choice.key }) {
                                Text(choice.text + suffix, style = MaterialTheme.typography.titleMedium)
                            }
                        }
                        if (selected != null) Text(if (selected == question.correctKey) labels.text("Correct!", "Richtig!")
                            else labels.text("Incorrect. The correct answer is highlighted.", "Falsch. Die richtige Antwort ist markiert."))
                    }
                }
                "results" -> {
                    val correct = Practice.score(session.map { it.correctKey }, answers)
                    Text(labels.text("Practice complete", "Übung abgeschlossen"), style = MaterialTheme.typography.headlineMedium)
                    Text("$correct / ${session.size}", style = MaterialTheme.typography.displayMedium)
                    Text("${if (session.isEmpty()) 0 else correct * 100 / session.size}%")
                    Button(modifier = Modifier.fillMaxWidth(), onClick = { start(session, origin) }) { Text(labels.text("Repeat", "Wiederholen")) }
                    OutlinedButton(modifier = Modifier.fillMaxWidth(), onClick = { back() }) { Text(labels.text("Back to menu", "Zurück zum Menü")) }
                }
            }
        }
    }
}
