import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:provider/provider.dart';
import '../providers/ui_state_provider.dart';
import '../widgets/animated_gradient.dart';
import '../widgets/dynamic_component_renderer.dart';
import '../widgets/vortex_sphere.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          // Animated Gradient Background
          const AnimatedGradient(),

          // Main Content
          Consumer<UIStateProvider>(
            builder: (context, uiState, child) {
              return SafeArea(
                child: Stack(
                  children: [
                    // Main Content
                    SingleChildScrollView(
                      child: SizedBox(
                        height: MediaQuery.of(context).size.height,
                        child: AnimatedSwitcher(
                          duration: const Duration(milliseconds: 500),
                          child: _buildMainContent(context, uiState),
                        ),
                      ),
                    ),

                    // Action Button
                    Positioned(
                      bottom: MediaQuery.of(context).padding.bottom + 16,
                      left: 0,
                      right: 0,
                      child: Center(
                        child: _buildActionButton(context, uiState),
                      ),
                    ),
                  ],
                ),
              );
            },
          ),
        ],
      ),
    );
  }

  Widget _buildMainContent(BuildContext context, UIStateProvider uiState) {
    if (uiState.isLoading) {
      return const Center(
        child: VortexSphere(),
      ).animate().fadeIn(duration: 500.ms).scale(
            begin: const Offset(1.2, 1.2),
            end: const Offset(1, 1),
          );
    }

    if (uiState.uiData.isEmpty) {
      return Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Welcome to',
              style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                    color: Colors.white,
                    fontWeight: FontWeight.w300,
                  ),
            ),
            RichText(
              text: TextSpan(
                children: [
                  TextSpan(
                    text: 'Adaptive ',
                    style: Theme.of(context).textTheme.headlineLarge?.copyWith(
                          color: Colors.white,
                          fontWeight: FontWeight.w600,
                        ),
                  ),
                  TextSpan(
                    text: 'Interface',
                    style: Theme.of(context).textTheme.headlineLarge?.copyWith(
                          color: Colors.white,
                          fontWeight: FontWeight.w300,
                        ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ).animate().fadeIn(duration: 500.ms).slideY(begin: 0.1, end: 0);
    }

    return Padding(
      padding: const EdgeInsets.all(24.0),
      child: Container(
        decoration: BoxDecoration(
          color: Colors.white.withOpacity(0.1),
          borderRadius: BorderRadius.circular(16),
        ),
        padding: const EdgeInsets.all(24),
        child: DynamicComponentRenderer(
          componentData: uiState.uiData,
          onStoreData: uiState.storeData,
          onSubmit: uiState.handleSubmit,
        ),
      ),
    ).animate().fadeIn(duration: 500.ms).slideY(begin: 0.1, end: 0);
  }

  Widget _buildActionButton(BuildContext context, UIStateProvider uiState) {
    return Container(
      width: 320,
      height: 56,
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.2),
        borderRadius: BorderRadius.circular(28),
      ),
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          onTap: uiState.uiData.isEmpty ? uiState.fetchDataFromAPI : uiState.reset,
          borderRadius: BorderRadius.circular(28),
          child: Center(
            child: Text(
              uiState.uiData.isEmpty ? 'Start' : 'Reset',
              style: Theme.of(context).textTheme.titleMedium?.copyWith(
                    color: Colors.white,
                  ),
            ),
          ),
        ),
      ),
    ).animate().fadeIn(duration: 500.ms).slideY(begin: 0.2, end: 0);
  }
} 