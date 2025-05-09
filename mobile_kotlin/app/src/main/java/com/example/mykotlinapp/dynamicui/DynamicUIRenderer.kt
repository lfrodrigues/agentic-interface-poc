package com.example.mykotlinapp.dynamicui

import android.content.Context
import android.text.Editable
import android.text.TextWatcher
import android.view.View
import android.view.ViewGroup
import android.widget.LinearLayout
import android.widget.TextView
import com.google.android.material.button.MaterialButton
import com.google.android.material.textfield.TextInputEditText
import com.google.android.material.textfield.TextInputLayout
import kotlinx.serialization.json.* // For JsonElement, JsonObject, JsonArray, JsonPrimitive

// Type alias for our component factory functions
typealias ComponentFactory = (
    context: Context,
    componentNode: ComponentNode, // Pass the whole node for access to props and children structure
    actionHandler: (actionName: String, actionParams: Map<String, String>?) -> Unit,
    json: Json // Pass Json instance for deserializing nested children
) -> View

// The map of component type strings to their factory functions
val androidComponentMap: Map<String, ComponentFactory> = mapOf(
    "Text" to ::createTextComponent,
    "View" to ::createViewComponent, // Represents a container like LinearLayout
    "Button" to ::createButtonComponent,
    "TextInput" to ::createTextInputComponent // Added TextInput
    // We'll add more components like "TextInput", "Image" later
)

// Main function to render a ComponentNode
fun renderNode(
    context: Context,
    node: ComponentNode,
    actionHandler: (actionName: String, actionParams: Map<String, String>?) -> Unit,
    jsonParser: Json = Json { ignoreUnknownKeys = true; coerceInputValues = true } // Default Json parser
): View? {
    val factory = androidComponentMap[node.type]
    return factory?.invoke(context, node, actionHandler, jsonParser)
        ?: run {
            println("Warning: Component type \"${node.type}\" is not supported.")
            // Optionally return a placeholder TextView for unsupported components
            TextView(context).apply { text = "Unsupported: ${node.type}" }
        }
}

// --- Placeholder/Simple Component Factory Implementations ---

fun createTextComponent(
    context: Context,
    node: ComponentNode,
    actionHandler: (actionName: String, actionParams: Map<String, String>?) -> Unit,
    json: Json
): View {
    val textView = TextView(context)
    // Text content can be directly in props (e.g., props.text) or as a simple string child
    val textContent = node.props?.get("text")?.jsonPrimitive?.contentOrNull ?:
                      node.children?.jsonPrimitive?.contentOrNull ?:
                      "Text" // Default text

    textView.text = textContent
    // Apply other props like textSize, textColor, etc. later
    node.props?.get("textSize")?.jsonPrimitive?.floatOrNull?.let { textView.textSize = it }
    // Example: how to parse a color string if you have one
    // node.props?.get("textColor")?.jsonPrimitive?.contentOrNull?.let { textView.setTextColor(Color.parseColor(it)) }


    return textView
}

fun createViewComponent(
    context: Context,
    node: ComponentNode,
    actionHandler: (actionName: String, actionParams: Map<String, String>?) -> Unit,
    json: Json
): View {
    // Using LinearLayout as a default container for "View" type
    val layout = LinearLayout(context).apply {
        orientation = LinearLayout.VERTICAL // Default orientation, can be made configurable via props
    }

    // Process children
    when (val childrenElement = node.children) {
        is JsonArray -> {
            childrenElement.forEach { childJsonElement ->
                try {
                    val childNode = json.decodeFromJsonElement<ComponentNode>(childJsonElement)
                    renderNode(context, childNode, actionHandler, json)?.let { layout.addView(it) }
                } catch (e: Exception) {
                    println("Error deserializing child node: $e")
                    // Add a placeholder for deserialization error
                    layout.addView(TextView(context).apply{ text = "Error rendering child"})
                }
            }
        }
        is JsonObject -> { // Single child object
            try {
                val childNode = json.decodeFromJsonElement<ComponentNode>(childrenElement)
                renderNode(context, childNode, actionHandler, json)?.let { layout.addView(it) }
            } catch (e: Exception) {
                println("Error deserializing single child object: $e")
                layout.addView(TextView(context).apply{ text = "Error rendering child"})
            }
        }
        is JsonPrimitive -> { // If children is a string, treat it as text content for the View (less common for 'View')
             if (childrenElement.isString) {
                layout.addView(TextView(context).apply { text = childrenElement.content })
             }
        }
        null -> { /* No children */ }
    }
    return layout
}

fun createButtonComponent(
    context: Context,
    node: ComponentNode,
    actionHandler: (actionName: String, actionParams: Map<String, String>?) -> Unit,
    json: Json
): View {
    val button = MaterialButton(context)
    button.text = node.props?.get("text")?.jsonPrimitive?.contentOrNull ?: "Button"

    val onPressAction = node.props?.get("onPress")?.jsonPrimitive?.contentOrNull
    if (onPressAction != null) {
        // Extract action parameters if they exist (example: props.onPressParams: {"id": "123"})
        val actionParamsMap = node.props?.get("onPressParams")?.jsonObject?.let { paramsObj ->
            paramsObj.mapValues { entry -> entry.value.jsonPrimitive.content }
        }
        button.setOnClickListener {
            actionHandler(onPressAction, actionParamsMap)
        }
    }
    // Add children to button? Typically buttons don't have complex children other than text.
    // If children were present and were a string, it could be button text, but we prioritize props.text
    return button
}

fun createTextInputComponent(
    context: Context,
    node: ComponentNode,
    actionHandler: (actionName: String, actionParams: Map<String, String>?) -> Unit,
    json: Json
): View {
    val textInputLayout = TextInputLayout(context).apply {
        layoutParams = LinearLayout.LayoutParams(
            LinearLayout.LayoutParams.MATCH_PARENT,
            LinearLayout.LayoutParams.WRAP_CONTENT
        )
        // ನೀವು ಇಲ್ಲಿ ಪ್ಯಾಡಿಂಗ್ ಅಥವಾ ಅಂಚುಗಳನ್ನು ಹೊಂದಿಸಬಹುದು
        // setPadding(0, 8, 0, 8) // Example padding (ವಾಸ್ತವಿಕ ಮೌಲ್ಯಗಳಿಗೆ dp ಬಳಸಿ)
    }

    val editText = TextInputEditText(textInputLayout.context)
    textInputLayout.addView(editText)

    val placeholderValue = node.props?.get("placeholder")?.jsonPrimitive?.contentOrNull
    val hintValue = node.props?.get("hint")?.jsonPrimitive?.contentOrNull
    val labelValue = node.props?.get("label")?.jsonPrimitive?.contentOrNull

    textInputLayout.hint = placeholderValue ?: hintValue ?: labelValue ?: "Enter text"

    val initialValue = node.props?.get("value")?.jsonPrimitive?.contentOrNull
    if (initialValue != null) {
        editText.setText(initialValue)
    }

    val fieldName = node.props?.get("name")?.jsonPrimitive?.contentOrNull ?: "unknownField"
    val onChangeTextAction = node.props?.get("onChangeText")?.jsonPrimitive?.contentOrNull

    if (onChangeTextAction != null && fieldName != null) {
        editText.addTextChangedListener(object : TextWatcher {
            override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {}
            override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {
                // Call the action handler with the action name from props and the current text
                actionHandler(onChangeTextAction, mapOf("name" to fieldName, "value" to s.toString()))
            }
            override fun afterTextChanged(s: Editable?) {}
        })
    }
    return textInputLayout
}

// TODO:
// - Implement more component factories (Image, etc.)
// - Add more robust props parsing (e.g., for styles, colors, dimensions, from props or "className"-like interpretation)
// - Action handler logic refinement
// - Error handling and logging 