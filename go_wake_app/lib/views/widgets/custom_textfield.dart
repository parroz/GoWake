import 'package:flutter/material.dart';

import '../login/login_controller.dart';

class CustomTextField extends StatelessWidget {
    CustomTextField({
    Key? key,
    required this.label,
    required this.icon,
    required this.input,
    required this.textController,
    required this.obscureText,
  });

  final String label;
  final IconData icon;
  final TextInputType input;
  final TextEditingController textController;
  final bool obscureText;

  @override
  Widget build(BuildContext context) {

    return TextFormField(
      keyboardType: input,
      controller: textController,
      obscureText: obscureText,
      onChanged: (value) {},
      validator: (value) {
        if (value!.isEmpty) {
          return "Mandatory field";
        }
      },
      decoration: InputDecoration(
        labelText: label,
        suffixIcon: Icon(icon),
      ),
    );
  }
  }

