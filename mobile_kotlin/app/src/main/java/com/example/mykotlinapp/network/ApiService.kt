package com.example.mykotlinapp.network

import io.ktor.client.* 
import io.ktor.client.engine.cio.* 
import io.ktor.client.plugins.contentnegotiation.* 
import io.ktor.client.request.* 
import io.ktor.client.statement.* 
import io.ktor.client.call.body
import io.ktor.http.* 
import io.ktor.serialization.kotlinx.json.* 
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement

// --- Data classes for API communication ---
@Serializable
data class ApiRequest(
    val message: String,
    val session_id: String
)

@Serializable
data class ApiResponse(
    val session_id: String,
    // Using JsonElement for message because the Expo app's setUiData
    // could receive a string or a component structure.
    // Our ComponentNode is expecting a JSON object/array for UI.
    val message: JsonElement
)

// --- Ktor HTTP Client Setup ---
object ApiClient {
    // Use 10.0.2.2 for Android Emulator to connect to localhost on the host machine
    // For a real device on the same Wi-Fi, use your computer's network IP.
    // The Ngrok URL from the Expo app: https://fd24-217-165-28-125.ngrok-free.app/api/
    // For local development if your server is on http://localhost:3000
//    private const val BASE_URL = "http://10.0.2.2:3000/api/" // Emulator default for localhost
     private const val BASE_URL = "https://0b32-94-202-179-120.ngrok-free.app/api/" // ngrok URL with /api/
//

    val client = HttpClient(CIO) {
        install(ContentNegotiation) {
            json(Json {
                prettyPrint = true
                isLenient = true
                ignoreUnknownKeys = true // Important for flexibility
                coerceInputValues = true
            })
        }
        // Optional: Logging, default request headers, etc.
        // install(Logging) { level = LogLevel.ALL }
    }

    suspend fun fetchInitialUI(): ApiResponse {
        val requestBody = ApiRequest(message = "NEW", session_id = "NEW")
        return client.post(BASE_URL) {
            contentType(ContentType.Application.Json)
            setBody(requestBody)
        }.body() // Ktor will deserialize to ApiResponse
    }

    suspend fun submitData(sessionId: String, formDataJson: String): ApiResponse {
        // The Expo app sends formDataJson directly as the 'message' field's value
        val requestBody = ApiRequest(message = formDataJson, session_id = sessionId)
        return client.post(BASE_URL) {
            contentType(ContentType.Application.Json)
            setBody(requestBody)
        }.body()
    }
} 