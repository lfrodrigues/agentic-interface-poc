package com.example.mykotlinapp.dynamicui

import kotlinx.serialization.Serializable
import kotlinx.serialization.json.JsonElement

@Serializable
data class ComponentNode(
    val type: String,
    val props: Map<String, JsonElement>? = null,
    val children: JsonElement? = null // Can be JsonPrimitive (string), JsonObject (single child node), or JsonArray (list of child nodes)
) 