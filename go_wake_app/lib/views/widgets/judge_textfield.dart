import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:go_wake_app/models/leaderboard.dart';

import '../judge/judge_controller.dart';

class CustomJudgeTextField extends StatelessWidget {
  CustomJudgeTextField({
    Key? key,
    required this.label,
    required this.input,
    required this.textController,
    required this.controller,
  });

  final String label;
  final TextInputType input;
  final TextEditingController textController;
  final JudgeController controller;
  @override
  Widget build(BuildContext context) {
    return  Column(
      children: [
        Container(
          width: 60,
          height: 60,
          decoration: BoxDecoration(
            color: Theme.of(context).colorScheme.surfaceVariant,
            border: Border.all(color: Colors.black),
            borderRadius: BorderRadius.all(Radius.circular(5)),
          ),
          child: Center(
            child: TextFormField(
              onChanged: (value) {

                  if(value!= null){
                    controller.validateJudgeText(value.toString(),label);
                  }

              },
              validator: (value) {
                  if(value!= null){
                    double? pontuation = double.tryParse(value);
                    if (pontuation != null) {
                      if(pontuation > 10)
                        return "Max pontuation is 10";
                    }
                  }
                if (value!.isEmpty) {
                  return "Mandatory field";
                }
              },
              controller: textController,
              textAlign: TextAlign.center,
              style: TextStyle(fontSize: 20, color: Theme.of(context).colorScheme.onPrimary,),
              decoration: InputDecoration(
                border: InputBorder.none,
              ),
              keyboardType: TextInputType.numberWithOptions(decimal: true),
              inputFormatters: [
                FilteringTextInputFormatter.allow(RegExp(r'^\d+\.?\d*$')),
                LengthLimitingTextInputFormatter(3),
              ],
            ),
          ),
        ),      Text(
           label,
          style: TextStyle(
              color: Theme.of(context)
                  .colorScheme
                  .onSecondaryContainer,
              fontSize: 15),
        ),
      ],
    );
  }
}
