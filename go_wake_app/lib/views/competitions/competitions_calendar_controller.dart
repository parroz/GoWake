import 'package:flutter/cupertino.dart';
import 'package:go_wake_app/models/competition.dart';

import '../../services/services.dart';
import '../../shared/constants.dart';

class CompetitionCalendarController extends ChangeNotifier  {
  LoginState _state = LoginState.LOADING;
  LoginState get state => _state;
  String _errorMsg = "";
  String get errorMsg => _errorMsg;
  ResultCompetition _resultCompetition = ResultCompetition() ;
  ResultCompetition get resultCompetition => _resultCompetition;

  Future<void> getCompetitions() async {
    try {
      final Services service = Services ();
      _resultCompetition = await service.getCompetitions();

      if(_resultCompetition.competitions != null){
        _state = LoginState.SUCCESS;
      }else{
        _state = LoginState.FAIL;
        _errorMsg = "";
      }
      notifyListeners();
    } catch (error) {
      _errorMsg = error.toString();
      _state = LoginState.FAIL;
      notifyListeners();
    }
  }

  void onsortColum(int columnIndex, bool ascending,  List<Competition> competitions) {
    if(columnIndex==0){
      if (ascending) {
        _resultCompetition.competitions!.sort((a, b) => a.beginningDate!.compareTo(b.beginningDate!));
      } else {
        _resultCompetition.competitions!.sort((a, b) => b.beginningDate!.compareTo(a.beginningDate!));
      }
    }
      if(columnIndex==4){
        if (ascending) {
          _resultCompetition.competitions!.sort((a, b) => a.name!.toLowerCase().compareTo(b.name!.toLowerCase()));
        } else {
          _resultCompetition.competitions!.sort((a, b) => b.name!.toLowerCase().compareTo(a.name!.toLowerCase()));
        }
      }
      if(columnIndex==1){
        if (ascending) {
          _resultCompetition.competitions!.sort((a, b) => a.discipline!.toLowerCase().compareTo(b.discipline!.toLowerCase()));
        } else {
          _resultCompetition.competitions!.sort((a, b) => b.discipline!.toLowerCase().compareTo(a.discipline!.toLowerCase()));
        }
      }
      if(columnIndex==2){
        if (ascending) {
          _resultCompetition.competitions!.sort((a, b) => a.tournamentType!.toLowerCase().compareTo(b.tournamentType!.toLowerCase()));
        } else {
          _resultCompetition.competitions!.sort((a, b) => b.tournamentType!.toLowerCase().compareTo(a.tournamentType!.toLowerCase()));
        }
      }
      if(columnIndex==3){
        if (ascending) {
          _resultCompetition.competitions!.sort((a, b) => a.organizingCountry!.toLowerCase().compareTo(b.organizingCountry!.toLowerCase()));
        } else {
          _resultCompetition.competitions!.sort((a, b) => b.organizingCountry!.toLowerCase().compareTo(a.organizingCountry!.toLowerCase()));
        }
      }

    notifyListeners();
  }


}