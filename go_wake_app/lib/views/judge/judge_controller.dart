import 'package:flutter/cupertino.dart';

import '../../models/auth.dart';
import '../../models/competition_detail.dart';

import '../../models/judge_leaderboard.dart';
import '../../services/service_locator.dart';
import '../../services/services.dart';
import '../../shared/constants.dart';
import '../../storage/secure_storage_service .dart';
import 'package:connectivity_plus/connectivity_plus.dart';

class JudgeController extends ChangeNotifier  {
  LoginState _state = LoginState.LOADING;
  LoginState get state => _state;
  String _errorMsg = "";
  String get errorMsg => _errorMsg;
  late LeaderboardJudge _leaderboard ;
  LeaderboardJudge get  leaderboard => _leaderboard;
  final intController = TextEditingController();
  final compController = TextEditingController();
  final execController = TextEditingController();
  final notesController = TextEditingController();

  Future<void> getLeaderboard(String id) async {
    compController.clear();
    intController.clear();
    execController.clear();
    notesController.clear();

    try {
      final Services service = Services ();
      _leaderboard = await service.getLeaderboard(id);
      if(_leaderboard != null){
        final SecureStorageService _secureStorageService =
        serviceLocator<SecureStorageService>();
        final iwwfId = await _secureStorageService.getIwwfId();

        if(_leaderboard.q1stJudgeIwwfId == iwwfId.toString()){
          _leaderboard.JudgeAtlheteFrontFoot = _leaderboard.q1stJudgeAtlheteFrontFoot!;
          _leaderboard.JudgeCompositionScore = _leaderboard.q1stJudgeCompositionScore!;
          _leaderboard.JudgeExecutionScore = _leaderboard.q1stJudgeExecutionScore!;
          _leaderboard.JudgeIntensityScore = _leaderboard.q1stJudgeIntensityScore!;
          _leaderboard.JudgeGlobalScore = _leaderboard.q1stJudgeGlobalScore!;
          _leaderboard.JudgeFallsCount = _leaderboard.q1stJudgeFallsCount!;
          _leaderboard.JudgeNotes = _leaderboard.q1stJudgeNotes!;
          _leaderboard.JudgeRotationsCount = _leaderboard.q1stJudgeRotationsCount!;
          _leaderboard.JudgeTricksCount = _leaderboard.q1stJudgeTricksCount!;
          _leaderboard.JudgeInvertsCount = _leaderboard.q1stJudgeInvertsCount!;
        }
        if(_leaderboard.q2ndJudgeIwwfId == iwwfId.toString()){
          _leaderboard.JudgeAtlheteFrontFoot = _leaderboard.q2ndJudgeAtlheteFrontFoot!;
          _leaderboard.JudgeCompositionScore = _leaderboard.q2ndJudgeCompositionScore!;
          _leaderboard.JudgeExecutionScore = _leaderboard.q2ndJudgeExecutionScore!;
          _leaderboard.JudgeIntensityScore = _leaderboard.q2ndJudgeIntensityScore!;
          _leaderboard.JudgeGlobalScore = _leaderboard.q2ndJudgeGlobalScore!;
          _leaderboard.JudgeFallsCount = _leaderboard.q2ndJudgeFallsCount!;
          _leaderboard.JudgeNotes = _leaderboard.q2ndJudgeNotes!;
          _leaderboard.JudgeRotationsCount = _leaderboard.q2ndJudgeRotationsCount!;
          _leaderboard.JudgeTricksCount = _leaderboard.q2ndJudgeTricksCount!;
          _leaderboard.JudgeInvertsCount = _leaderboard.q2ndJudgeInvertsCount!;
        }
        if(_leaderboard.q3rdJudgeIwwfId == iwwfId.toString()){
          _leaderboard.JudgeAtlheteFrontFoot = _leaderboard.q3rdJudgeAtlheteFrontFoot!;
          _leaderboard.JudgeCompositionScore = _leaderboard.q3rdJudgeCompositionScore!;
          _leaderboard.JudgeExecutionScore = _leaderboard.q3rdJudgeExecutionScore!;
          _leaderboard.JudgeIntensityScore = _leaderboard.q3rdJudgeIntensityScore!;
          _leaderboard.JudgeGlobalScore = _leaderboard.q3rdJudgeGlobalScore!;
          _leaderboard.JudgeFallsCount = _leaderboard.q3rdJudgeFallsCount!;
          _leaderboard.JudgeNotes = _leaderboard.q3rdJudgeNotes!;
          _leaderboard.JudgeRotationsCount = _leaderboard.q3rdJudgeRotationsCount!;
          _leaderboard.JudgeTricksCount = _leaderboard.q3rdJudgeTricksCount!;
          _leaderboard.JudgeInvertsCount = _leaderboard.q3rdJudgeInvertsCount!;
        }
        if(_leaderboard.JudgeCompositionScore > 0)
           compController.text =_leaderboard.JudgeCompositionScore.toString();
        if(_leaderboard.JudgeIntensityScore > 0)
           intController.text=_leaderboard.JudgeIntensityScore.toString();
        if(_leaderboard.JudgeExecutionScore > 0)
           execController.text=_leaderboard.JudgeExecutionScore.toString();

        notesController.text=_leaderboard.JudgeNotes.toString();

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

  void setJudgeAtlheteFrontFoot(String foot) {
    _leaderboard.JudgeAtlheteFrontFoot =foot;
    notifyListeners();
  }

  void addJudgeCounts(String origin) {
    if(origin== 'T'){
      _leaderboard.JudgeTricksCount ++;
    }
    if(origin== 'Inv'){
      _leaderboard.JudgeInvertsCount ++;
    }
    if(origin== 'Rot'){
      _leaderboard.JudgeRotationsCount ++;
    }
    if(origin== 'F'){
      _leaderboard.JudgeFallsCount ++;
    }
    notifyListeners();
  }

  Future<void>  updateJudgeSheet() async {
    final connectivityResult = await (Connectivity().checkConnectivity());
    final Services service = Services ();
    final SecureStorageService _secureStorageService =
    serviceLocator<SecureStorageService>();
    final iwwfId = await _secureStorageService.getIwwfId();

    if(_leaderboard.q1stJudgeIwwfId == iwwfId.toString()){
      if (compController.text.trim().isNotEmpty) {
        _leaderboard.q1stJudgeCompositionScore = double.parse(compController.text);
      }
      if (intController.text.trim().isNotEmpty) {
        _leaderboard.q1stJudgeIntensityScore = double.parse(intController.text);
      }
      if (execController.text.trim().isNotEmpty) {
        _leaderboard.q1stJudgeExecutionScore = double.parse(execController.text);
      }
      if (notesController.text.trim().isNotEmpty) {
        _leaderboard.q1stJudgeNotes = notesController.text;
      }
      _leaderboard.q1stJudgeTricksCount= _leaderboard.JudgeTricksCount;
      _leaderboard.q1stJudgeInvertsCount= _leaderboard.JudgeInvertsCount;
      _leaderboard.q1stJudgeRotationsCount= _leaderboard.JudgeRotationsCount;
      _leaderboard.q1stJudgeFallsCount= _leaderboard.JudgeFallsCount;
      _leaderboard.q1stJudgeAtlheteFrontFoot = _leaderboard.JudgeAtlheteFrontFoot;
    }

    if(_leaderboard.q2ndJudgeIwwfId == iwwfId.toString()){
      if (compController.text.trim().isNotEmpty) {
        _leaderboard.q2ndJudgeCompositionScore = double.parse(compController.text);
      }
      if (intController.text.trim().isNotEmpty) {
        _leaderboard.q2ndJudgeIntensityScore = double.parse(intController.text);
      }
      if (execController.text.trim().isNotEmpty) {
        _leaderboard.q2ndJudgeExecutionScore = double.parse(execController.text);
      }
      if (notesController.text.trim().isNotEmpty) {
        _leaderboard.q2ndJudgeNotes = notesController.text;
      }
      _leaderboard.q2ndJudgeTricksCount= _leaderboard.JudgeTricksCount;
      _leaderboard.q2ndJudgeInvertsCount= _leaderboard.JudgeInvertsCount;
      _leaderboard.q2ndJudgeRotationsCount= _leaderboard.JudgeRotationsCount;
      _leaderboard.q2ndJudgeFallsCount= _leaderboard.JudgeFallsCount;
      _leaderboard.q2ndJudgeAtlheteFrontFoot = _leaderboard.JudgeAtlheteFrontFoot;
    }
    if(_leaderboard.q3rdJudgeIwwfId == iwwfId.toString()){
      if (compController.text.trim().isNotEmpty) {
        _leaderboard.q3rdJudgeCompositionScore = double.parse(compController.text);
      }
      if (intController.text.trim().isNotEmpty) {
        _leaderboard.q3rdJudgeIntensityScore = double.parse(intController.text);
      }
      if (execController.text.trim().isNotEmpty) {
        _leaderboard.q3rdJudgeExecutionScore = double.parse(execController.text);
      }
      if (notesController.text.trim().isNotEmpty) {
        _leaderboard.q3rdJudgeNotes = notesController.text;
      }
        _leaderboard.q3rdJudgeTricksCount= _leaderboard.JudgeTricksCount;
        _leaderboard.q3rdJudgeInvertsCount= _leaderboard.JudgeInvertsCount;
        _leaderboard.q3rdJudgeRotationsCount= _leaderboard.JudgeRotationsCount;
        _leaderboard.q3rdJudgeFallsCount= _leaderboard.JudgeFallsCount;

      _leaderboard.q3rdJudgeAtlheteFrontFoot = _leaderboard.JudgeAtlheteFrontFoot;
    }
    try {
      if (connectivityResult == ConnectivityResult.wifi||
          connectivityResult == ConnectivityResult.mobile) {
        _state = LoginState.LOADING;
        notifyListeners();
        _leaderboard=  await service.updateJudgeSheet(_leaderboard);
        _state = LoginState.SUCCESS;
      }
      notifyListeners();
    } catch (error) {
      _errorMsg = error.toString();
      _state = LoginState.FAIL;
      notifyListeners();
    }


  }

  void validateJudgeText(String text, String label) {
    double? pontuation = double.tryParse(text);
    if (pontuation != null) {
      if(pontuation > 10){
        if(label=="Int.")
          intController.text ="";
        if(label=="Comp.")
          compController.text ="";
        if(label=="exec.")
          execController.text ="";
        notifyListeners();
      }

    }
  }



}