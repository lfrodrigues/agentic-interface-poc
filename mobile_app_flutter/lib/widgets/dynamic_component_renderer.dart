import 'package:flutter/material.dart';
import 'dart:convert';

class DynamicComponentRenderer extends StatelessWidget {
  final Map<String, dynamic> componentData;
  final Function(String, String) onStoreData;
  final VoidCallback onSubmit;

  const DynamicComponentRenderer({
    super.key,
    required this.componentData,
    required this.onStoreData,
    required this.onSubmit,
  });

  @override
  Widget build(BuildContext context) {
    try {
      return _buildComponent(context, componentData);
    } catch (e) {
      return const Center(
        child: Text(
          'Error rendering component',
          style: TextStyle(color: Colors.white),
        ),
      );
    }
  }

  Widget _buildComponent(BuildContext context, dynamic data) {
    if (data is Map<String, dynamic>) {
      final type = data['type'] as String?;
      final props = data['props'] as Map<String, dynamic>?;
      final children = data['children'];

      switch (type?.toLowerCase()) {
        case 'view':
          return Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              if (children is List)
                ...children.map((child) => _buildComponent(context, child)).toList()
              else if (children != null)
                _buildComponent(context, children),
            ],
          );

        case 'text':
          return Text(
            children?.toString() ?? '',
            style: const TextStyle(
              color: Colors.white,
              fontSize: 16,
            ),
          );

        case 'textinput':
          return TextField(
            style: const TextStyle(color: Colors.white),
            decoration: InputDecoration(
              hintText: props?['placeholder'] ?? '',
              hintStyle: TextStyle(color: Colors.white.withOpacity(0.5)),
              enabledBorder: OutlineInputBorder(
                borderSide: BorderSide(color: Colors.white.withOpacity(0.2)),
                borderRadius: BorderRadius.circular(8),
              ),
              focusedBorder: OutlineInputBorder(
                borderSide: const BorderSide(color: Colors.white),
                borderRadius: BorderRadius.circular(8),
              ),
            ),
            onChanged: (value) => onStoreData(props?['name'] ?? '', value),
          );

        case 'button':
          return ElevatedButton(
            onPressed: onSubmit,
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.white.withOpacity(0.2),
              foregroundColor: Colors.white,
              padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(8),
              ),
            ),
            child: Text(props?['title'] ?? 'Submit'),
          );

        default:
          return const SizedBox.shrink();
      }
    }
    return const SizedBox.shrink();
  }
} 