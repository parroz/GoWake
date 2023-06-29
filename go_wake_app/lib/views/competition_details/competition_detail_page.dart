import 'package:flag/flag_widget.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:go_wake_app/models/competition_detail.dart';
import 'package:go_wake_app/models/leaderboard.dart';
import 'package:provider/provider.dart';

import '../../shared/constants.dart';
import '../../shared/extensions.dart';
import '../judge/judge_page.dart';
import '../widgets/error_dialog.dart';
import 'competition_detail_controller.dart';

class CompetitionDetailPage extends StatefulWidget {
  const CompetitionDetailPage(this.id, {Key? key}) : super(key: key);
  final String id;

  @override
  State<CompetitionDetailPage> createState() => _CompetitionDetailPageState();
}

class _CompetitionDetailPageState extends State<CompetitionDetailPage> {
  late String id;
  bool judgeView = true;
  int row_index =0;
  List<DataRow> dataRows = [];
  @override
  void initState() {
    super.initState();
    var controller =
        Provider.of<CompetitionDetailController>(context, listen: false);
    controller.getCompetitionDetail(widget.id);
    controller.addListener(() {
      if (controller.state == LoginState.FAIL) {
        ShowErrorDialog(controller.errorMsg, context);
      }
    });
  }

  @override
  Widget build(BuildContext context) {

    List<DataRow> generateDataRows( controller, category,judgeView) {
      return  controller.leaderboard.results.map((leaderboard) {
        return DataRow(cells: [
          DataCell(SizedBox(
            child: Text(leaderboard.qStartingList.toString()),
            width: 30,
          )),

           DataCell(
        IgnorePointer(
            ignoring: !leaderboard.canJudge,
           child: GestureDetector(
              child: Icon(Icons.edit),
              onTap: () {
                  Navigator.pop(context);
                  Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => JudgePage(leaderboard.id.toString()),
                  ),
                );

              },

            )),
          ),

          DataCell(Text(leaderboard.athlete!.firstName + " "+
              leaderboard.athlete!.lastName)),
          DataCell(Flag.fromCode(
            Extensions.getFlagCode(
                leaderboard.athlete!.country),
            height: 30,
            width: 40,
            fit: BoxFit.fill,
          )),
          DataCell(Text(category)),
          DataCell(Text(leaderboard!.qPlacement.toString())),
          if (judgeView)...[
            DataCell(Text(leaderboard!.JudgeGlobalScore.toString())),
            DataCell(Text(leaderboard!.JudgeIntensityScore.toString())),
            DataCell(Text(leaderboard!.JudgeExecutionScore.toString())),
            DataCell(Text(leaderboard!.JudgeCompositionScore.toString())),
        ]
         else...[
             DataCell(Text(leaderboard!.qGlobalScore.toString())),
             DataCell(Text(leaderboard!.qGlobalIntensityScore.toString())),
             DataCell(Text(leaderboard!.qGlobalExecutionScore.toString())),
             DataCell(Text(leaderboard!.qGlobalCompositionScore.toString())),
            ]


        ]);
      }).toList().cast<DataRow>();
    }
    return Material(
      child: Scaffold(
        appBar: AppBar(centerTitle: true,
          title:  Image.asset(
            'lib/assets/logo_bar.png',
            height: 30,
          ),),
        body: SingleChildScrollView(
            padding: const EdgeInsets.fromLTRB(10.0, 30.0, 10.0, 0.0),
            child: Consumer<CompetitionDetailController>(
                builder: (BuildContext context, controller, widget) {
              return (controller.state == LoginState.LOADING)
                  ? const Center(
                      child: CircularProgressIndicator(
                        valueColor: AlwaysStoppedAnimation(Color(0xFF044EA8)),
                      ),
                    )
                  : Column(
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: <Widget>[
                        SizedBox(
                          width: double.infinity,
                          height: 200.0,
                          child: Card(
                            color:  Theme.of(context).colorScheme.background,
                              surfaceTintColor:
                                  Theme.of(context).colorScheme.background,
                              elevation: 10,
                              child: Padding(
                                padding: EdgeInsets.symmetric(
                                    vertical: 10.0, horizontal: 16.0),
                                child: Column(
                                    crossAxisAlignment:
                                        CrossAxisAlignment.start,
                                    children: <Widget>[
                                      Align(
                                        alignment: Alignment.topLeft,
                                        child: Flag.fromCode(
                                          Extensions.getFlagCode(controller
                                              .competitionDetail
                                              .organizingCountry),
                                          height: 70,
                                          width: 90,
                                          fit: BoxFit.fill,
                                        ),
                                      ),
                                      const SizedBox(
                                        height: 5,
                                      ),
                                      Text(
                                        controller.competitionDetail.name,
                                        style: TextStyle(
                                          fontWeight: FontWeight.bold,
                                          fontSize: 13,
                                          color:  Theme.of(context).colorScheme.onPrimary
                                        ),
                                      ),
                                      const SizedBox(
                                        height: 5,
                                      ),
                                      Text(
                                        controller.competitionDetail.venue,
                                        style: TextStyle(
                                          fontSize: 13,
                                          color:  Theme.of(context).colorScheme.onPrimary,
                                        ),
                                      ),
                                      const SizedBox(
                                        height: 10,
                                      ),
                                      Align(
                                        alignment: Alignment.bottomRight,
                                        child: Text(
                                          controller
                                              .competitionDetail.discipline,
                                          style: TextStyle(
                                            fontWeight: FontWeight.bold,
                                            fontSize: 13,
                                            color:  Theme.of(context).colorScheme.onPrimary
                                          ),
                                        ),
                                      ),
                                      Align(
                                        alignment: Alignment.bottomRight,
                                        child: Text(
                                          'Code: ' +
                                              controller.competitionDetail.code,
                                          style: TextStyle(
                                            fontSize: 13,
                                            color: Theme.of(context).colorScheme.onPrimary,
                                          ),
                                        ),
                                      ),
                                    ]),
                              )),
                        ),
                        SingleChildScrollView(scrollDirection: Axis.vertical,
                          child: SizedBox(
                            width: double.infinity,
                            height: null,
                            child: Card(
                              color: Theme.of(context).colorScheme.background,
                              surfaceTintColor:
                                  Theme.of(context).colorScheme.background,
                              elevation: 10,
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.stretch,
                                children: [
                                  Center(
                                    child: Text(
                                      "Leaderboard",
                                      style: TextStyle(
                                          color: Theme.of(context)
                                              .colorScheme
                                              .primary,
                                          fontWeight: FontWeight.bold,
                                          fontSize: 20),
                                    ),
                                  ),
                                  Row(
                                    mainAxisAlignment: MainAxisAlignment.center,
                                    children: [
                                      Text('Global view'),
                                      Switch(

                                          activeTrackColor:  Theme.of(context)
                                              .colorScheme
                                              .primaryContainer,
                                          value: judgeView,
                                          thumbColor:
                                              const MaterialStatePropertyAll<
                                                  Color>(Colors.white),
                                          onChanged: (bool value) {

                                            List<DataRow> rows = generateDataRows(controller,  controller
                                              .competitionDetail.categories[row_index].athleteCategoryInCompetition!,value);

                                            setState(() {
                                               dataRows = rows;
                                              judgeView = value;

                                            });
                                          }),
                                      Text('Judge view'),
                                    ],
                                  ),
                                  Container(
                                    child: ExpansionPanelList(

                                      expansionCallback: (int index, bool isExpanded) {
                                        controller
                                            .competitionDetail.categories[index].expanded =!isExpanded;
                                        controller.getLeaderboards(controller
                                            .competitionDetail.categories[index]).then((leaderboards) {
                                          row_index = index;
                                          List<DataRow> rows = generateDataRows(controller,  controller
                                              .competitionDetail.categories[index].athleteCategoryInCompetition!,judgeView);

                                          setState(() {
                                            dataRows = rows;
                                          });
                                        });
                                      },
                                      children: controller
                                          .competitionDetail.categories
                                          .map<ExpansionPanel>(
                                              (Category item) {
                                        return ExpansionPanel(
                                            isExpanded: item.expanded,
                                            headerBuilder:
                                                (BuildContext context,
                                                    bool isExpanded) {
                                              return ListTile(
                                                title: Text(item
                                                    .athleteCategoryInCompetition! + " " + item.athleteGender! + " " + item.round! + " Heat "+ item.q_heat_number!),
                                              );
                                            },
                                            body: ListTile(

                                              title: SingleChildScrollView(
                                                scrollDirection:
                                                    Axis.horizontal,
                                                child: DataTable(
                                                  columns: [
                                                    DataColumn(
                                                        label: SizedBox(
                                                      child: Text('Start'),
                                                      width: 30,
                                                    )),
                                                    DataColumn(
                                                        label: Text(' ')),
                                                    DataColumn(
                                                        label: Text('Name')),
                                                    DataColumn(
                                                        label: Text('Country')),
                                                    DataColumn(
                                                        label:
                                                            Text('Category')),
                                                    DataColumn(
                                                        label: Text('Place')),
                                                    DataColumn(
                                                        label: Text('Score')),
                                                    DataColumn(
                                                        label: Text('Int.')),
                                                    DataColumn(
                                                        label: Text('Comp.')),
                                                    DataColumn(
                                                        label: Text('Exec.')),
                                                  ],
                                                  rows: dataRows,

                                                ),
                                              ),
                                            ));
                                      }).toList(),
                                    ),
                                  )
                                ],
                              ),
                            ),
                          ),
                        ),
                      ],
                    );
            })),
      ),
    );
  }
}
