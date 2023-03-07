
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

class CustomButtom extends StatelessWidget {
  CustomButtom({
    Key? key,
    required this.onPressed,
    required this.textcolor,
    required this.text,
    required this.backgroundcolor,
  });

  final Function onPressed;
  final Color   textcolor;
  final Color  backgroundcolor;
  final String text;

  @override
  Widget build(BuildContext context) {

    return   ElevatedButton(
      onPressed: () => onPressed(),
      style: ElevatedButton.styleFrom(
        backgroundColor: backgroundcolor,
        foregroundColor: textcolor,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(0), // <-- Radius
        ),
        padding: const EdgeInsets.symmetric(
          horizontal: 30,
          vertical: 8,
        ),
      ),
      child:   Text(
        text,
      ),
    );
  }
}