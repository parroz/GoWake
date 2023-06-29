import 'package:flutter/cupertino.dart';

import '../../models/auth.dart';
import '../../models/competition_detail.dart';
import '../../models/leaderboard.dart';
import '../../services/service_locator.dart';
import '../../services/services.dart';
import '../../shared/constants.dart';
import '../../storage/secure_storage_service .dart';

class CompetitionDetailController extends ChangeNotifier  {
  LoginState _state = LoginState.LOADING;
  LoginState get state => _state;
  String _errorMsg = "";
  String get errorMsg => _errorMsg;
  CompetitionDetail _competitionDetail = CompetitionDetail() ;
  CompetitionDetail get competitionDetail => _competitionDetail;
  ResultLeaderboard _leaderboard = ResultLeaderboard();
  ResultLeaderboard get  leaderboard => _leaderboard;
  Future<void> getCompetitionDetail(String id) async {
    try {
      final Services service = Services ();
      _competitionDetail = await service.getCompetitionDetail(id);
      if(_competitionDetail != null){
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

  Future<void> getLeaderboards(Category item) async {
    try {
      final Services service = Services ();
      _leaderboard = await service.getLeaderboards(item,_competitionDetail.id);
      if(_leaderboard != null){
        final SecureStorageService _secureStorageService =
        serviceLocator<SecureStorageService>();
        final iwwfId = await _secureStorageService.getIwwfId();
          _leaderboard.results.forEach((result) {
            if(result.q1stJudgeIwwfId == iwwfId.toString())
              result.canJudge = true;
            if(result.q2ndJudgeIwwfId == iwwfId.toString())
              result.canJudge = true;
            if(result.q3rdJudgeIwwfId == iwwfId.toString())
              result.canJudge = true;

              if(result.q1stJudgeIwwfId == iwwfId.toString()){
                result.JudgeIntensityScore = result.q1stJudgeIntensityScore!;
                result.JudgeExecutionScore = result.q1stJudgeExecutionScore!;
                result.JudgeCompositionScore = result.q1stJudgeCompositionScore!;
                result.JudgeGlobalScore = result.q1stJudgeGlobalScore!;
              }

              if(result.q2ndJudgeIwwfId == iwwfId.toString()){
                result.JudgeIntensityScore = result.q2ndJudgeIntensityScore!;
                result.JudgeExecutionScore = result.q2ndJudgeExecutionScore!;
                result.JudgeCompositionScore = result.q2ndJudgeCompositionScore!;
                result.JudgeGlobalScore = result.q2ndJudgeGlobalScore!;
              }

              if(result.q3rdJudgeIwwfId == iwwfId.toString()){
                result.JudgeIntensityScore = result.q3rdJudgeIntensityScore!;
                result.JudgeExecutionScore = result.q3rdJudgeExecutionScore!;
                result.JudgeCompositionScore = result.q3rdJudgeCompositionScore!;
                result.JudgeGlobalScore = result.q3rdJudgeGlobalScore!;
              }

          });

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

}