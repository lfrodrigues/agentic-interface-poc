package com.example.mykotlinapp

import android.os.Bundle
import android.util.Log
import com.google.android.material.snackbar.Snackbar
import androidx.appcompat.app.AppCompatActivity
import android.view.Menu
import android.view.MenuItem
import android.widget.TextView
import android.widget.Toast
import androidx.lifecycle.lifecycleScope
import com.example.mykotlinapp.databinding.ActivityMainBinding
import com.example.mykotlinapp.dynamicui.ComponentNode
import com.example.mykotlinapp.dynamicui.renderNode
import com.example.mykotlinapp.network.ApiClient
import com.example.mykotlinapp.network.ApiResponse
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonElement

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding
    private val jsonParser = Json { ignoreUnknownKeys = true; coerceInputValues = true; prettyPrint = true }

    private var currentSessionId: String? = null
    private val formData = mutableMapOf<String, String>()

    companion object {
        private const val TAG = "MainActivity"
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)
        setSupportActionBar(binding.toolbar)

        binding.fab.setOnClickListener { view ->
            Snackbar.make(view, "FAB Clicked", Snackbar.LENGTH_LONG).show()
        }

        val loadButton = binding.contentMainLayout.loadUiButton
        val dynamicContainer = binding.contentMainLayout.dynamicUiContainer

        loadButton.setOnClickListener {
            dynamicContainer.removeAllViews()
            val loadingView = TextView(this).apply { text = "Fetching initial UI..." }
            dynamicContainer.addView(loadingView)

            lifecycleScope.launch {
                try {
                    val apiResponse = withContext(Dispatchers.IO) {
                        ApiClient.fetchInitialUI()
                    }
                    currentSessionId = apiResponse.session_id
                    formData.clear() // Clear form data on new UI load
                    Log.d(TAG, "Initial API Response: $apiResponse")
                    processAndRenderApiResponse(apiResponse, dynamicContainer)
                } catch (e: Exception) {
                    Log.e(TAG, "Error fetching initial UI", e)
                    handleApiError(e, dynamicContainer)
                }
            }
        }
    }

    private fun dynamicActionHandler(actionName: String, actionParams: Map<String, String>?) {
        Log.d(TAG, "Action: $actionName, Params: $actionParams")
        when (actionName) {
            "storeData" -> {
                val fieldName = actionParams?.get("name")
                val fieldValue = actionParams?.get("value") // Assuming value is passed this way
                if (fieldName != null && fieldValue != null) {
                    formData[fieldName] = fieldValue
                    Log.d(TAG, "Stored data: $formData")
                    // Optionally, show a quick toast or update some local state if needed
                    // Toast.makeText(this, "$fieldName stored", Toast.LENGTH_SHORT).show()
                } else {
                    Log.w(TAG, "storeData action called without proper name/value params")
                }
            }
            "handleSubmit" -> {
                handleSubmitData()
            }
            else -> {
                val paramsString = actionParams?.entries?.joinToString() ?: "No params"
                Toast.makeText(this, "Unhandled Action: $actionName, Params: $paramsString", Toast.LENGTH_LONG).show()
            }
        }
    }

    private fun handleSubmitData() {
        val sessionId = currentSessionId
        if (sessionId == null) {
            Toast.makeText(this, "Session ID is missing.", Toast.LENGTH_SHORT).show()
            Log.w(TAG, "handleSubmitData called without session ID")
            return
        }

        val dynamicContainer = binding.contentMainLayout.dynamicUiContainer
        dynamicContainer.removeAllViews()
        val loadingView = TextView(this).apply { text = "Submitting data..." }
        dynamicContainer.addView(loadingView)

        lifecycleScope.launch {
            try {
                Log.d(TAG, "handleSubmitData - formData before serialization: $formData")
                val formDataJsonString = jsonParser.encodeToString(formData)
                Log.d(TAG, "Submitting formData JSON string: $formDataJsonString with sessionId: $sessionId")
                val apiResponse = withContext(Dispatchers.IO) {
                    ApiClient.submitData(sessionId, formDataJsonString)
                }
                currentSessionId = apiResponse.session_id // Update session ID if backend sends a new one
                formData.clear() // Clear form data after successful submission
                Log.d(TAG, "Submit API Response: $apiResponse")
                processAndRenderApiResponse(apiResponse, dynamicContainer)
            } catch (e: Exception) {
                Log.e(TAG, "Error submitting data", e)
                handleApiError(e, dynamicContainer)
            }
        }
    }

    private fun processAndRenderApiResponse(apiResponse: ApiResponse, container: android.widget.LinearLayout) {
        container.removeAllViews()
        try {
            // The 'message' from API is JsonElement. We need to parse it into ComponentNode.
            // This assumes apiResponse.message is a JSON representation of a ComponentNode.
            val componentNode = jsonParser.decodeFromJsonElement(ComponentNode.serializer(), apiResponse.message)
            val dynamicView = renderNode(this@MainActivity, componentNode, ::dynamicActionHandler, jsonParser)

            if (dynamicView != null) {
                container.addView(dynamicView)
            } else {
                Toast.makeText(this@MainActivity, "Failed to render dynamic UI from API", Toast.LENGTH_SHORT).show()
            }
        } catch (e: Exception) {
            Log.e(TAG, "Error parsing/rendering API response message: ${apiResponse.message}", e)
            handleApiError(JsonParsingException("Error processing UI data from server: ${e.message}", e), container)
        }
    }

    private fun handleApiError(exception: Exception, container: android.widget.LinearLayout) {
        container.removeAllViews()
        Toast.makeText(this@MainActivity, "API Error: ${exception.message}", Toast.LENGTH_LONG).show()
        val errorView = TextView(this@MainActivity)
        errorView.text = "Error: ${exception.localizedMessage}"
        container.addView(errorView)
    }

    // Custom exception for better context
    class JsonParsingException(message: String, cause: Throwable? = null) : Exception(message, cause)

    override fun onCreateOptionsMenu(menu: Menu): Boolean {
        menuInflater.inflate(R.menu.menu_main, menu)
        return true
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        return when (item.itemId) {
            R.id.action_settings -> true
            else -> super.onOptionsItemSelected(item)
        }
    }
}