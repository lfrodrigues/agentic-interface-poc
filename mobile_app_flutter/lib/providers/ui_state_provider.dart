import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;

class UIStateProvider extends ChangeNotifier {
  Map<String, dynamic> _uiData = {};
  bool _isLoading = false;
  String _sessionId = '';
  Map<String, String> _formData = {};

  Map<String, dynamic> get uiData => _uiData;
  bool get isLoading => _isLoading;
  String get sessionId => _sessionId;

  void setUiData(Map<String, dynamic> data) {
    _uiData = data;
    notifyListeners();
  }

  void setLoading(bool loading) {
    _isLoading = loading;
    notifyListeners();
  }

  void storeData(String name, String value) {
    _formData[name] = value;
  }

  void reset() {
    _uiData = {};
    _formData = {};
    notifyListeners();
  }

  Future<void> fetchDataFromAPI() async {
    try {
      setLoading(true);
      final response = await http.post(
        Uri.parse('https://fd24-217-165-28-125.ngrok-free.app/api/talk/'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'message': 'NEW',
          'session_id': 'NEW'
        }),
      );
      
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        _sessionId = data['session_id'];
        _formData = {};
        setUiData(data['message']);
      } else {
        throw Exception('Failed to fetch data: ${response.statusCode}');
      }
    } catch (error) {
      print('Error fetching UI data: $error');
      setUiData({});
    } finally {
      setLoading(false);
    }
  }

  Future<void> handleSubmit() async {
    try {
      setLoading(true);
      final response = await http.post(
        Uri.parse('https://fd24-217-165-28-125.ngrok-free.app/api/talk/'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'session_id': _sessionId,
          'message': json.encode(_formData)
        }),
      );
      
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        _formData = {};
        setUiData(data['message'] as Map<String, dynamic>);
      } else {
        throw Exception('Failed to submit form: ${response.statusCode}');
      }
    } catch (error) {
      print('Error submitting form: $error');
    } finally {
      setLoading(false);
    }
  }
} 