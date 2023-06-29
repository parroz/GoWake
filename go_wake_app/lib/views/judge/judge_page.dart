import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../shared/constants.dart';
import '../competition_details/competition_detail_page.dart';
import '../widgets/custom_button.dart';
import '../widgets/error_dialog.dart';
import '../widgets/judge_textfield.dart';
import 'judge_controller.dart';

class JudgePage extends StatefulWidget {
  const JudgePage(this.id, {Key? key}) : super(key: key);
  final String id;

  @override
  State<JudgePage> createState() => _JudgePagePageState();
}

class _JudgePagePageState extends State<JudgePage> {
  String selectedLetter = "L";
  final _formKeyValidator = GlobalKey<FormState>();

  @override
  void initState() {
    super.initState();
    var controller = Provider.of<JudgeController>(context, listen: false);
    controller.getLeaderboard(widget.id);
    controller.addListener(() {
      if (controller.state == LoginState.FAIL) {
        ShowErrorDialog(controller.errorMsg, context);
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Material(
      child: Scaffold(
        appBar: AppBar(centerTitle: true,
          title:  Image.asset(
            'lib/assets/logo_bar.png',
            height: 30,
          ),),
        body: SingleChildScrollView(
          padding: const EdgeInsets.fromLTRB(5.0, 30.0, 5.0, 0.0),
          child: Consumer<JudgeController>(
              builder: (BuildContext context, controller, widget) {
            return (controller.state == LoginState.LOADING)
                ? const Center(
                    child: CircularProgressIndicator(
                      valueColor: AlwaysStoppedAnimation(Color(0xFF044EA8)),
                    ),
                  )
                : Card(
                    surfaceTintColor: Theme.of(context).colorScheme.background,
                    color:Theme.of(context).colorScheme.background,
                    elevation: 10,
                    child: Padding(
                      padding: EdgeInsets.symmetric(
                          vertical: 10.0, horizontal: 16.0),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.stretch,
                        children: [
                          Center(
                            child: Text(
                              "Judge sheet",
                              style: TextStyle(
                                  color: Theme.of(context).colorScheme.primary,
                                  fontWeight: FontWeight.bold,
                                  fontSize: 20),
                            ),
                          ),
                          SizedBox(
                            height: 10,
                          ),
                          Center(
                            child: Text(
                              controller.leaderboard
                                      .athleteCategoryInCompetition! +
                                  "/" +
                                  controller.leaderboard.round! +
                                  "/ Heat " +
                                  controller.leaderboard.qHeatNumber! +
                                  "/ Rider " +
                                  controller.leaderboard.qStartingList
                                      .toString(),
                              style: TextStyle(
                                  color: Theme.of(context)
                                      .colorScheme
                                      .onSecondaryContainer,
                                  fontSize: 15),
                            ),
                          ),
                          SizedBox(
                            height: 10,
                          ),
                          Center(
                              child: Container(
                            decoration: BoxDecoration(
                              color: Theme.of(context).colorScheme.background,
                              border: Border.all(
                                color: Colors.black,
                                width: 1.0,
                              ),
                            ),
                            child: Text(
                              " ${controller.leaderboard.athlete?.firstName!} ${controller.leaderboard.athlete?.lastName!} ",
                              style: TextStyle(fontSize: 16),
                            ),
                          )),
                          SizedBox(
                            height: 20,
                          ),
                          Row(
                            children: [
                              Text(
                                "Front foot: ",
                                style: TextStyle(
                                    color: Theme.of(context)
                                        .colorScheme
                                        .onSecondaryContainer,
                                    fontSize: 15),
                              ),
                              SizedBox(width: 20),
                              GestureDetector(
                                onTap: () {
                                  controller.setJudgeAtlheteFrontFoot('L');
                                },
                                child: Container(
                                  width: 50,
                                  height: 50,
                                  decoration: BoxDecoration(
                                    color: controller.leaderboard
                                                .JudgeAtlheteFrontFoot ==
                                            'L'
                                        ? Colors.black
                                        : Colors.grey,
                                    border: Border.all(color: Colors.black),
                                    borderRadius:
                                        BorderRadius.all(Radius.circular(5)),
                                  ),
                                  child: Center(
                                    child: Text(
                                      'L',
                                      style: TextStyle(
                                          fontSize: 20, color: Colors.white),
                                    ),
                                  ),
                                ),
                              ),
                              SizedBox(width: 10),
                              GestureDetector(
                                onTap: () {
                                  controller.setJudgeAtlheteFrontFoot('R');
                                },
                                child: Container(
                                  width: 50,
                                  height: 50,
                                  decoration: BoxDecoration(
                                    color: controller.leaderboard
                                                .JudgeAtlheteFrontFoot ==
                                            'R'
                                        ? Colors.black
                                        : Colors.grey,
                                    border: Border.all(color: Colors.black),
                                    borderRadius:
                                        BorderRadius.all(Radius.circular(5)),
                                  ),
                                  child: Center(
                                    child: Text(
                                      'R',
                                      style: TextStyle(
                                          fontSize: 20, color: Colors.white),
                                    ),
                                  ),
                                ),
                              ),
                              SizedBox(width: 72),
                              Column(
                                children: [
                                  Container(
                                    width: 60,
                                    height: 60,
                                    decoration: BoxDecoration(
                                      color: Theme.of(context)
                                          .colorScheme
                                          .primaryContainer,
                                      border: Border.all(color: Colors.black),
                                      borderRadius:
                                          BorderRadius.all(Radius.circular(5)),
                                    ),
                                    child: Center(
                                      child: Text(
                                        controller.leaderboard.placementText
                                            .toString(),
                                        style: TextStyle(
                                            fontSize: 20, color: Colors.white),
                                      ),
                                    ),
                                  ),
                                  Text(
                                    "Place",
                                    style: TextStyle(
                                        color: Theme.of(context)
                                            .colorScheme
                                            .onSecondaryContainer,
                                        fontSize: 15),
                                  ),
                                ],
                              )
                            ],
                          ),
                          SizedBox(height: 32),
                          Form(
                            key: _formKeyValidator,
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.stretch,
                              children: [
                                Row(children: [
                                  CustomJudgeTextField(
                                    label: "Int.",
                                    input: TextInputType.number,
                                    textController: controller.intController,
                                      controller:controller
                                  ),
                                  const SizedBox(
                                    width: 20,
                                  ),
                                  CustomJudgeTextField(
                                    label: "Comp.",
                                    input: TextInputType.number,
                                    textController: controller.compController,
                                      controller:controller
                                  ),
                                  const SizedBox(
                                    width: 20,
                                  ),
                                  CustomJudgeTextField(
                                    label: "exec.",
                                    input: TextInputType.number,
                                    textController: controller.execController,
                                      controller:controller
                                  ),
                                  SizedBox(width: 60),
                                  Column(
                                    children: [
                                      Container(
                                        width: 60,
                                        height: 60,
                                        decoration: BoxDecoration(
                                          color: Theme.of(context)
                                              .colorScheme
                                              .primaryContainer,
                                          border:
                                              Border.all(color: Colors.black),
                                          borderRadius: BorderRadius.all(
                                              Radius.circular(5)),
                                        ),
                                        child: Center(
                                          child: Text(
                                            controller
                                                .leaderboard.JudgeGlobalScore
                                                .toString(),
                                            style: TextStyle(
                                                fontSize: 20,
                                                color: Colors.white),
                                          ),
                                        ),
                                      ),
                                      Text(
                                        "Score",
                                        style: TextStyle(
                                            color: Theme.of(context)
                                                .colorScheme
                                                .onSecondaryContainer,
                                            fontSize: 15),
                                      ),
                                    ],
                                  ),
                                ]),
                                SizedBox(height: 20),
                                Row(
                                  children: [
                                    SizedBox(
                                      height: 50,
                                      child: ElevatedButton(

                                        onPressed: () {
                                          controller.addJudgeCounts('T');
                                        },
                                        style: ElevatedButton.styleFrom(
                                          shape: RoundedRectangleBorder(
                                            borderRadius:
                                            BorderRadius.circular(5),
                                          ),
                                          primary: Colors.green, // Set the button's background color
                                        ),
                                        child: Text('T',
                                            style: TextStyle(
                                              color: Colors.white,
                                            )), // Set the button's label
                                      ),
                                    ),
                                    SizedBox(width: 15),
                                    SizedBox(
                                      height: 50,
                                      child: ElevatedButton(
                                        onPressed: () {
                                          controller.addJudgeCounts('Inv');
                                        },
                                        style: ElevatedButton.styleFrom(
                                          shape: RoundedRectangleBorder(
                                            borderRadius:
                                                BorderRadius.circular(5),
                                          ),
                                          primary: Colors
                                              .orange, // Set the button's background color
                                        ),
                                        child: Text(
                                            'Inv',
                                            style: TextStyle(
                                              color: Colors.white,
                                            )), // Set the button's label
                                      ),
                                    ),
                                    SizedBox(width: 15),
                                    SizedBox(
                                   height: 50,
                                      child: ElevatedButton(

                                        onPressed: () {
                                          controller.addJudgeCounts('Rot');
                                        },
                                        style: ElevatedButton.styleFrom(
                                          shape: RoundedRectangleBorder(
                                            borderRadius:
                                                BorderRadius.circular(5),
                                          ),
                                          primary: Theme.of(context)
                                              .colorScheme
                                              .primaryContainer,
                                        ),
                                        child: Text('Rot',
                                            style: TextStyle(
                                              color: Colors.white,
                                            )),
                                      ),
                                    ),
                                    SizedBox(width: 55),
                                    SizedBox(
                                      height: 50,
                                      child: ElevatedButton(
                                        onPressed: () {
                                          controller.addJudgeCounts('F');
                                        },
                                        style: ElevatedButton.styleFrom(
                                          shape: RoundedRectangleBorder(
                                            borderRadius:
                                                BorderRadius.circular(5),
                                          ),
                                          primary: Colors
                                              .red, // Set the button's background color
                                        ),
                                        child:
                                            Text('F',
                                                style: TextStyle(
                                                  color: Colors.white,
                                                )), // Set the button's label
                                      ),
                                    ),
                                  ],
                                ),SizedBox(height: 20),
                                Center(
                                  child: TextField(
                                    controller: controller.notesController,
                                    maxLines: null,
                                    textAlign: TextAlign.left,
                                    decoration: InputDecoration(
                                      fillColor: Theme.of(context).colorScheme.surfaceVariant,
                                      hintText: 'Write your notes here...',
                                      border: OutlineInputBorder(),
                                    ),
                                  ),
                                ),
                                SizedBox(height: 20),
                                Row(
                                  children: [
                                    SizedBox(width: 20),
                                    Column(
                                      children: [
                                        Container(
                                          width: 50,
                                          height: 50,
                                          decoration: BoxDecoration(
                                            color: Theme.of(context)
                                                .colorScheme
                                                .onSecondary,
                                            border:
                                            Border.all(color: Colors.green),
                                            borderRadius: BorderRadius.all(
                                                Radius.circular(5)),
                                          ),
                                          child: Center(
                                            child: Text(
                                              controller
                                                  .leaderboard.JudgeTricksCount
                                                  .toString(),
                                              style: TextStyle(
                                                  fontSize: 20,
                                                  color: Colors.green),
                                            ),
                                          ),
                                        ),
                                        Text(
                                          "Tricks",
                                          style: TextStyle(
                                              color: Colors.green,
                                              fontSize: 10),
                                        ),
                                      ],
                                    ), SizedBox(width: 30),

                                        Column(
                                          children: [
                                            Container(
                                              width: 50,
                                              height: 50,
                                              decoration: BoxDecoration(
                                                color: Theme.of(context)
                                                    .colorScheme
                                                    .onSecondary,
                                                border:
                                                Border.all(color: Colors.orange),
                                                borderRadius: BorderRadius.all(
                                                    Radius.circular(5)),
                                              ),
                                              child: Center(
                                                child: Text(
                                                  controller
                                                      .leaderboard.JudgeInvertsCount
                                                      .toString(),
                                                  style: TextStyle(
                                                      fontSize: 20,
                                                      color: Colors.orange),
                                                ),
                                              ),
                                            ),
                                            Text(
                                              "Inverts",
                                              style: TextStyle(
                                                  color: Colors.orange,
                                                  fontSize: 10),
                                            ),
                                          ],
                                        ), SizedBox(width: 30),
                                    Column(
                                      children: [
                                        Container(
                                          width: 50,
                                          height: 50,
                                          decoration: BoxDecoration(
                                            color: Theme.of(context)
                                                .colorScheme
                                                .onSecondary,
                                            border:
                                            Border.all(color:Theme.of(context)
                                                .colorScheme
                                                .primaryContainer,),
                                            borderRadius: BorderRadius.all(
                                                Radius.circular(5)),
                                          ),
                                          child: Center(
                                            child: Text(
                                              controller
                                                  .leaderboard.JudgeRotationsCount
                                                  .toString(),
                                              style: TextStyle(
                                                  fontSize: 20,
                                                  color: Theme.of(context)
                                                      .colorScheme
                                                      .primaryContainer,),
                                            ),
                                          ),
                                        ),
                                        Text(
                                          "Rotations",
                                          style: TextStyle(
                                              color:Theme.of(context)
                                                  .colorScheme
                                                  .primaryContainer,
                                              fontSize: 10),
                                        ),
                                      ],
                                    ), SizedBox(width: 30),
                                    Column(
                                      children: [
                                        Container(
                                          width: 50,
                                          height: 50,
                                          decoration: BoxDecoration(
                                            color: Theme.of(context)
                                                .colorScheme
                                                .onSecondary,
                                            border:
                                            Border.all(color: Colors.red),
                                            borderRadius: BorderRadius.all(
                                                Radius.circular(5)),
                                          ),
                                          child: Center(
                                            child: Text(
                                              controller
                                                  .leaderboard.JudgeFallsCount
                                                  .toString(),
                                              style: TextStyle(
                                                  fontSize: 20,
                                                  color: Colors.red),
                                            ),
                                          ),
                                        ),
                                        Text(
                                          "Fails",
                                          style: TextStyle(
                                              color: Colors.red,
                                              fontSize: 10),
                                        ),
                                      ],
                                    ), SizedBox(width: 30),
                                  ],
                                ),
                                SizedBox(height: 10),
                                if(!controller.leaderboard.qValidated!)
                                  CustomButtom(
                                    onPressed: () {
                                      if (_formKeyValidator.currentState!.validate()) {
                                        controller.updateJudgeSheet();
                                          Navigator.pushReplacement(
                                            context,
                                           MaterialPageRoute(builder: (context) => CompetitionDetailPage(controller.leaderboard.competition.toString())), // Replace the current page with OtherPage
                                         );
                                       // Navigator.pop(context); // Pop the current page
                                       // Navigator.pop(context, true);

                                      }
                                    },
                                    textcolor: Colors.white,
                                    text: 'Submit',
                                    backgroundcolor: const Color(0xFF044EA8),
                                  )

                            , ],
                            ),
                          ),
                        ],
                      ),
                    ),
                  );
          }),
        ),
      ),
    );
  }
}
