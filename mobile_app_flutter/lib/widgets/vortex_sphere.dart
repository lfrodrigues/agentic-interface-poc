import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';

class VortexSphere extends StatelessWidget {
  const VortexSphere({super.key});

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 100,
      height: 100,
      child: Stack(
        children: List.generate(3, (index) {
          return Container(
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              border: Border.all(
                color: Colors.white.withOpacity(0.2),
                width: 2,
              ),
            ),
          ).animate(
            onPlay: (controller) => controller.repeat(),
          ).animate(
            onPlay: (controller) => controller.repeat(),
          ).scale(
            begin: const Offset(0.8, 0.8),
            end: const Offset(1.2, 1.2),
            duration: 1.seconds,
            curve: Curves.easeInOut,
          ).animate(
            onPlay: (controller) => controller.repeat(),
          ).rotate(
            begin: 0,
            end: 1,
            duration: 2.seconds,
            curve: Curves.linear,
          );
        }),
      ),
    );
  }
} 