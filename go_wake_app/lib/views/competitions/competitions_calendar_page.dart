
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:go_wake_app/models/competition.dart';
import 'package:go_wake_app/views/competition_details/competition_detail_page.dart';
import 'package:go_wake_app/views/competitions/competitions_calendar_controller.dart';
import 'package:intl/intl.dart';
import 'package:provider/provider.dart';
import 'package:flag/flag.dart';
import '../../shared/constants.dart';
import '../../shared/extensions.dart';
import '../../utils/app_routes.dart';
import '../widgets/error_dialog.dart';

class CompetitionsCalendarPage extends StatefulWidget {
  const CompetitionsCalendarPage({Key? key}) : super(key: key);

  @override
  State<CompetitionsCalendarPage> createState() =>
      _CompetitionsCalendarPageState();
}

class _CompetitionsCalendarPageState extends State<CompetitionsCalendarPage> {
  bool sort = true;
  TextEditingController filterController = TextEditingController();
  int _columnIndex = 0;

  @override
  void initState() {
    super.initState();
    var controller =
        Provider.of<CompetitionCalendarController>(context, listen: false);
    controller.getCompetitions();
    controller.addListener(() {
      if (controller.state == LoginState.FAIL) {
        ShowErrorDialog(controller.errorMsg, context);
      }
    });
  }

  @override
  Widget build(BuildContext context) {

    return Scaffold(
        body: Container(
            padding: const EdgeInsets.all(8.0),
            decoration: BoxDecoration(
              color: Theme.of(context).canvasColor,
              borderRadius: const BorderRadius.all(Radius.circular(10)),
            ),
            child:
                Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                    Padding(
                      padding: EdgeInsets.only(right: 0, top: 40,bottom: 20),
                      child: Center(
                        child: Text(
                        "Events Calendar",
                        style: TextStyle(color: Theme.of(context).colorScheme.primary,
                            fontWeight: FontWeight.bold, fontSize: 20),
                  ),
                      ),
                    ),
              Consumer<CompetitionCalendarController>(
                  builder: (BuildContext context, controller, widget) {
                return SizedBox(
                    width: double.infinity,
                    child: (controller.state == LoginState.LOADING)
                        ? const Center(
                            child: CircularProgressIndicator(
                              valueColor:
                                  AlwaysStoppedAnimation(Color(0xFF044EA8)),
                            ),
                          )
                        : Card(elevation: 10,
                      color: Theme.of(context).colorScheme.background,
                      surfaceTintColor:
                      Theme.of(context).colorScheme.background,
                          child: PaginatedDataTable(
                              sortColumnIndex: _columnIndex,
                              sortAscending: sort,
                              source: RowSource(
                                context:context,
                                competitions:
                                    controller.resultCompetition.competitions,
                                count: controller
                                    .resultCompetition.competitions.length,
                              ),
                              rowsPerPage:  controller
                                  .resultCompetition.competitions.length <=5?controller
                                  .resultCompetition.competitions.length: 5,
                              columns: [
                                  DataColumn(
                                      label: const Text(
                                        "Beggining Date",
                                        style: TextStyle(
                                            fontWeight: FontWeight.bold,
                                            fontSize: 12),
                                      ),
                                      onSort: (columnIndex, ascending) {
                                        sortCell(columnIndex,ascending,controller);
                                      }),
                                  DataColumn(
                                      label: const Text(
                                        "Discipline",
                                        style: TextStyle(
                                            fontWeight: FontWeight.bold,
                                            fontSize: 12),
                                      ),
                                      onSort: (columnIndex, ascending) {
                                        sortCell(columnIndex,ascending,controller);
                                      }),
                                  DataColumn(
                                      label: const Text(
                                        "Type",
                                        style: TextStyle(
                                            fontWeight: FontWeight.bold,
                                            fontSize: 12),
                                      ),
                                      onSort: (columnIndex, ascending) {
                                        sortCell(columnIndex,ascending,controller);
                                      }),
                                  DataColumn(
                                      label: const Text(
                                        "Country",
                                        style: TextStyle(
                                            fontWeight: FontWeight.bold,
                                            fontSize: 12),
                                      ),
                                      onSort: (columnIndex, ascending) {
                                        sortCell(columnIndex,ascending,controller);
                                      }),
                                  DataColumn(
                                      label: const Text(
                                        "Name",
                                        style: TextStyle(
                                            fontWeight: FontWeight.bold,
                                            fontSize: 12),
                                      ),
                                      onSort: (columnIndex, ascending) {
                                        sortCell(columnIndex,ascending,controller);
                                      }),
                                  const DataColumn(
                                    label: Text(
                                      "",
                                      style: TextStyle(
                                          fontWeight: FontWeight.bold,
                                          fontSize: 0),
                                    ),
                                  ),
                                ]),
                        ));
              })
            ])));
  }

  void sortCell(int columnIndex, bool ascending, CompetitionCalendarController controller) {
    setState(() {
      sort = ascending;
      _columnIndex = columnIndex;
    });

    controller.onsortColum(
        columnIndex,
        ascending,
        controller
            .resultCompetition.competitions);
  }
}

class RowSource extends DataTableSource {
  List<Competition> competitions;
  final count;
  final context;

  RowSource(  {
    required this.competitions,
    required this.count, required BuildContext this.context,
  });

  @override
  DataRow? getRow(int index) {
    if (index < rowCount) {
      return recentFileDataRow(competitions![index],context);
    } else {
      return null;
    }
  }

  @override
  bool get isRowCountApproximate => false;

  @override
  int get rowCount => count;

  @override
  int get selectedRowCount => 0;
}

DataRow recentFileDataRow(Competition data, context) {
  void _competitionDetail(){
    Navigator.push(
      context,MaterialPageRoute(builder: (context)=>CompetitionDetailPage( data.id.toString())));
  }
  return DataRow(
    cells: [
      DataCell(
        GestureDetector(
            child: Text(DateFormat('yyyy-MM-dd').format(data.beginningDate!))),
        onDoubleTap: _competitionDetail,
      ),
      DataCell(
        GestureDetector(child: Text(data.discipline.toString())),
        onDoubleTap: _competitionDetail,
      ),
      DataCell(
        GestureDetector(child: Text(data.tournamentType.toString())),
        onDoubleTap: _competitionDetail,
      ),
      DataCell(Flag.fromCode(
        Extensions.getFlagCode(data.organizingCountry),
        height: 30,
        width: 40,
        fit: BoxFit.fill,
      )),
      DataCell(Text(data.name.toString())),
      DataCell(
        Visibility(
          visible: false,
          child: Text(
            data.id.toString(),
          ),
        ),
      ),
    ],
  );
}


