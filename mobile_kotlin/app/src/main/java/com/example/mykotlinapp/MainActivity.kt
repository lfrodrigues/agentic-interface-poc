package com.example.mykotlinapp

import android.os.Bundle
import com.google.android.material.snackbar.Snackbar
import androidx.appcompat.app.AppCompatActivity
import android.view.Menu
import android.view.MenuItem
import android.widget.LinearLayout
import android.widget.Toast
import android.widget.TextView
import com.example.mykotlinapp.databinding.ActivityMainBinding
import com.example.mykotlinapp.dynamicui.ComponentNode
import com.example.mykotlinapp.dynamicui.renderNode
import kotlinx.serialization.json.Json

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        setSupportActionBar(binding.toolbar)

        binding.fab.setOnClickListener { view ->
            Snackbar.make(view, "Replace with your own action", Snackbar.LENGTH_LONG)
                .setAction("Action", null)
                .show()
        }

        val dynamicContainer = binding.contentMainLayout.dynamicUiContainer

        val mockJson = """
            {
                "type": "View",
                "props": {},
                "children": [
                    {
                        "type": "Text",
                        "props": {"text": "Hello from Dynamic UI!", "textSize": 24.0}
                    },
                    {
                        "type": "Button",
                        "props": {"text": "Click Me!", "onPress": "handleButtonClick", "onPressParams": {"source": "mainButton"}}
                    },
                    {
                        "type": "Text",
                        "props": {"text": "LUIS."}
                    },
                    {
                        "type": "View",
                        "children": [
                             {
                                "type": "Text",
                                "props": {"text": "Nested Text in a Nested View"}
                             },
                             {
                                "type": "Button",
                                "props": {"text": "Nested Button", "onPress": "handleNestedButton"}
                             }
                        ]
                    }
                ]
            }
        """

        val actionHandler = { actionName: String, actionParams: Map<String, String>? ->
            val paramsString = actionParams?.entries?.joinToString() ?: "No params"
            Toast.makeText(this, "Action: $actionName, Params: $paramsString", Toast.LENGTH_LONG).show()
        }

        try {
            val jsonParser = Json { ignoreUnknownKeys = true; coerceInputValues = true }
            val componentNode = jsonParser.decodeFromString<ComponentNode>(mockJson)

            val dynamicView = renderNode(this, componentNode, actionHandler, jsonParser)
            if (dynamicView != null) {
                dynamicContainer.addView(dynamicView)
            } else {
                Toast.makeText(this, "Failed to render dynamic UI", Toast.LENGTH_SHORT).show()
            }
        } catch (e: Exception) {
            e.printStackTrace()
            Toast.makeText(this, "Error parsing or rendering UI: ${e.message}", Toast.LENGTH_LONG).show()
            val errorView = TextView(this)
            errorView.text = "Error loading UI: ${e.localizedMessage}"
            dynamicContainer.addView(errorView)
        }
    }

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