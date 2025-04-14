import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';

class AnimatedGradient extends StatelessWidget {
  const AnimatedGradient({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: [
            Colors.purple.shade900,
            Colors.deepPurple.shade900,
            Colors.indigo.shade900,
          ],
        ),
      ),
    ).animate(
      onPlay: (controller) => controller.repeat(),
    ).animate(
      onPlay: (controller) => controller.repeat(),
    ).shimmer(
      duration: 2.seconds,
      color: Colors.white.withOpacity(0.2),
    );
  }
} 