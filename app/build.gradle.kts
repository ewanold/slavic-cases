import com.android.build.api.artifact.SingleArtifact
import java.time.LocalDate
import java.time.ZoneOffset

plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.plugin.compose")
}
val localReleasePreview = providers.gradleProperty("localReleasePreview").map { it.toBoolean() }.getOrElse(false)

android {
    namespace = "org.slaviccases.app"
    compileSdk = 36
    buildToolsVersion = "36.0.0"
    defaultConfig {
        applicationId = "org.slaviccases.app"
        minSdk = 29
        targetSdk = 36
        versionCode = 2
        versionName = "0.2"
        val buildDate = LocalDate.now(ZoneOffset.UTC).toString()
        buildConfigField("String", "BUILD_DATE", "\"$buildDate\"")
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }
    buildTypes {
        getByName("debug") {
            buildConfigField("boolean", "ALLOW_DRAFT_CONTENT", "true")
        }
        getByName("release") {
            isDebuggable = false
            buildConfigField("boolean", "ALLOW_DRAFT_CONTENT", localReleasePreview.toString())
            if (localReleasePreview) signingConfig = signingConfigs.getByName("debug")
        }
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
    // Keep AGP's install metadata intact; provide stable names for sharing APKs.
    val exportApk = tasks.register<Copy>("export${variant.name.replaceFirstChar { it.uppercase() }}Apk") {
        from(variant.artifacts.get(SingleArtifact.APK)) {
            include("*.apk")
            rename { if (variant.buildType == "release") "learn-grammatical-cases.apk" else "learn-grammatical-cases-${variant.name}.apk" }
        }
        into(layout.buildDirectory.dir("distributions"))
    }
    tasks.matching { it.name == "assemble${variant.name.replaceFirstChar { it.uppercase() }}" }.configureEach {
        dependsOn(exportApk)
    }
}
// Draft lessons are explicitly allowed in debug; publishing requires review.
val validateReleaseContent by tasks.registering(Exec::class) {
        commandLine(providers.environmentVariable("CONTENT_PYTHON").getOrElse("python3"),
            rootProject.file("scripts/validate-samples.py").absolutePath, "--release")
}
tasks.matching { it.name == "preReleaseBuild" }.configureEach {
    if (!localReleasePreview) dependsOn(validateReleaseContent)
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
