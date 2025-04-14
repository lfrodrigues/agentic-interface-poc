# Adaptive Interface - Flutter Version

This is a Flutter implementation of the Adaptive Interface app, which provides a dynamic and responsive user interface that adapts based on server responses.

## Features

- Beautiful animated gradient background
- Dynamic component rendering from API responses
- Smooth animations and transitions
- Modern Material Design 3 UI
- Dark theme optimized

## Getting Started

### Prerequisites

- Flutter SDK (version 3.2.3 or higher)
- Dart SDK (version 3.0.0 or higher)
- Android Studio / VS Code with Flutter extensions
- iOS development tools (for iOS development)

### Installation

1. Clone the repository
2. Navigate to the project directory:
   ```bash
   cd mobile_app_flutter
   ```
3. Install dependencies:
   ```bash
   flutter pub get
   ```

### Running the App

1. Connect a device or start an emulator
2. Run the app:
   ```bash
   flutter run
   ```

## Project Structure

- `lib/`
  - `main.dart` - App entry point and theme configuration
  - `screens/` - Screen widgets
  - `widgets/` - Reusable UI components
  - `providers/` - State management
  - `models/` - Data models

## Dependencies

- `flutter_animate` - For smooth animations
- `provider` - For state management
- `http` - For API communication
- `google_fonts` - For custom typography
- `shared_preferences` - For local storage

## API Integration

The app communicates with a backend API to fetch dynamic UI components. The API endpoint is configured in the `UIStateProvider` class.

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request
