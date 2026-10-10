import java.time.LocalDate
import java.time.ZoneOffset

plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.plugin.compose")
}
android {
    namespace = "org.slaviccases.app"
    compileSdk = 36
    buildToolsVersion = "36.0.0"
    defaultConfig {
        applicationId = "org.slaviccases.app"
        minSdk = 29
        targetSdk = 36
        versionCode = 1
        versionName = "0.1"
        val buildDate = LocalDate.now(ZoneOffset.UTC).toString()
        buildConfigField("String", "BUILD_DATE", "\"$buildDate\"")
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }
    buildFeatures { compose = true; buildConfig = true }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
}
kotlin { compilerOptions { jvmTarget.set(org.jetbrains.kotlin.gradle.dsl.JvmTarget.JVM_17) } }
abstract class GenerateContent : Exec() {
    @get:OutputDirectory abstract val outputDirectory: DirectoryProperty
}
val generateContent by tasks.registering(GenerateContent::class) {
    environment("PYTHONDONTWRITEBYTECODE", "1")
    inputs.dir(rootProject.file("samples"))
    inputs.files(rootProject.file("scripts/package-content.py"), rootProject.file("scripts/validate-samples.py"))
    outputDirectory.set(layout.buildDirectory.dir("generated/content"))
    commandLine(providers.environmentVariable("CONTENT_PYTHON").getOrElse("python3"),
        rootProject.file("scripts/package-content.py").absolutePath,
        "--output", layout.buildDirectory.file("generated/content/content.json").get().asFile.absolutePath)
}
androidComponents.onVariants { variant ->
    variant.sources.assets?.addGeneratedSourceDirectory(generateContent, GenerateContent::outputDirectory)
}
// Draft lessons are explicitly allowed in debug; publishing requires review.
val validateReleaseContent by tasks.registering(Exec::class) {
        commandLine(providers.environmentVariable("CONTENT_PYTHON").getOrElse("python3"),
            rootProject.file("scripts/validate-samples.py").absolutePath, "--release")
}
tasks.matching { it.name == "preReleaseBuild" }.configureEach {
    dependsOn(validateReleaseContent)
}
dependencies {
    implementation(platform("androidx.compose:compose-bom:2026.04.01"))
    implementation("androidx.activity:activity-compose:1.10.1")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.compose.ui:ui-tooling-preview")
    debugImplementation("androidx.compose.ui:ui-tooling")
    testImplementation("junit:junit:4.13.2")
    androidTestImplementation(platform("androidx.compose:compose-bom:2026.04.01"))
    androidTestImplementation("androidx.compose.ui:ui-test-junit4")
    androidTestImplementation("androidx.test:runner:1.6.2")
    debugImplementation("androidx.compose.ui:ui-test-manifest")
}
