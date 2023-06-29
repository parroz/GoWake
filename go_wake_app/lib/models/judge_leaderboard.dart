import 'dart:ffi';

import 'leaderboard.dart';

class LeaderboardJudge {
  int? id;
  Athlete? athlete;
  String? username;
  String? athleteGender;
  String? athleteCategoryInCompetition;
  int? ranking;
  double? globalPontuation;
  bool? qValidated;
  String? round;
  String? qHeatNumber;
  int? qStartingList;
  String? q1stJudgeLastName;
  String? q1stJudgeFirstName;
  String? q1stJudgeIwwfId;
  String? q2ndJudgeLastName;
  String? q2ndJudgeFirstName;
  String? q2ndJudgeIwwfId;
  String? q3rdJudgeLastName;
  String? q3rdJudgeFirstName;
  String? q3rdJudgeIwwfId;
  String? q1stJudgeAtlheteFrontFoot;
  String? q2ndJudgeAtlheteFrontFoot;
  String? q3rdJudgeAtlheteFrontFoot;
  double? q1stJudgeIntensityScore;
  double? q2ndJudgeIntensityScore;
  double? q3rdJudgeIntensityScore;
  double? q1stJudgeExecutionScore;
  double? q2ndJudgeExecutionScore;
  double? q3rdJudgeExecutionScore;
  double? q1stJudgeCompositionScore;
  double? q2ndJudgeCompositionScore;
  double? q3rdJudgeCompositionScore;
  double? q1stJudgeGlobalScore;
  double? q2ndJudgeGlobalScore;
  double? q3rdJudgeGlobalScore;
  int? q1stJudgeTricksCount;
  int? q2ndJudgeTricksCount;
  int? q3rdJudgeTricksCount;
  int? q1stJudgeInvertsCount;
  int? q2ndJudgeInvertsCount;
  int? q3rdJudgeInvertsCount;
  int? q1stJudgeRotationsCount;
  int? q2ndJudgeRotationsCount;
  int? q3rdJudgeRotationsCount;
  int? q1stJudgeFallsCount;
  int? q2ndJudgeFallsCount;
  int? q3rdJudgeFallsCount;
  String? q1stJudgeNotes;
  String? q2ndJudgeNotes;
  String? q3rdJudgeNotes;
  String  JudgeNotes="";
  int  JudgeRotationsCount= 0;
  int  JudgeTricksCount= 0;
  int  JudgeInvertsCount= 0;
  String  JudgeAtlheteFrontFoot="";
  double  JudgeIntensityScore= 0;
  double  JudgeExecutionScore= 0;
  double  JudgeCompositionScore= 0;
  double  JudgeGlobalScore= 0;
  int  JudgeFallsCount= 0;
  double? qGlobalIntensityScore;
  double? qGlobalExecutionScore;
  double? qGlobalCompositionScore;
  double? qGlobalScore;
  double? qGlobalIntensityPontuation;
  double? qGlobalExecutionPontuation;
  double? qGlobalCompositionPontuation;
  double? qGlobalPontuation;
  int? qPlacement;
  int? competition;
  String? placementText;

  LeaderboardJudge(
      {this.id,
        this.athlete,
        this.username,
        this.athleteGender,
        this.athleteCategoryInCompetition,
        this.ranking,
        this.globalPontuation,
        this.qValidated,
        this.round,
        this.qHeatNumber,
        this.qStartingList,
        this.q1stJudgeLastName,
        this.q1stJudgeFirstName,
        this.q1stJudgeIwwfId,
        this.q2ndJudgeLastName,
        this.q2ndJudgeFirstName,
        this.q2ndJudgeIwwfId,
        this.q3rdJudgeLastName,
        this.q3rdJudgeFirstName,
        this.q3rdJudgeIwwfId,
        this.q1stJudgeAtlheteFrontFoot,
        this.q2ndJudgeAtlheteFrontFoot,
        this.q3rdJudgeAtlheteFrontFoot,
        this.q1stJudgeIntensityScore,
        this.q2ndJudgeIntensityScore,
        this.q3rdJudgeIntensityScore,
        this.q1stJudgeExecutionScore,
        this.q2ndJudgeExecutionScore,
        this.q3rdJudgeExecutionScore,
        this.q1stJudgeCompositionScore,
        this.q2ndJudgeCompositionScore,
        this.q3rdJudgeCompositionScore,
        this.q1stJudgeGlobalScore,
        this.q2ndJudgeGlobalScore,
        this.q3rdJudgeGlobalScore,
        this.q1stJudgeTricksCount,
        this.q2ndJudgeTricksCount,
        this.q3rdJudgeTricksCount,
        this.q1stJudgeInvertsCount,
        this.q2ndJudgeInvertsCount,
        this.q3rdJudgeInvertsCount,
        this.q1stJudgeRotationsCount,
        this.q2ndJudgeRotationsCount,
        this.q3rdJudgeRotationsCount,
        this.q1stJudgeFallsCount,
        this.q2ndJudgeFallsCount,
        this.q3rdJudgeFallsCount,
        this.q1stJudgeNotes,
        this.q2ndJudgeNotes,
        this.q3rdJudgeNotes,

        this.qGlobalIntensityScore,
        this.qGlobalExecutionScore,
        this.qGlobalCompositionScore,
        this.qGlobalScore,
        this.qGlobalIntensityPontuation,
        this.qGlobalExecutionPontuation,
        this.qGlobalCompositionPontuation,
        this.qGlobalPontuation,
        this.qPlacement,
        this.competition});

  LeaderboardJudge.fromJson(Map<String, dynamic> json) {
    id = json['id'];
    athlete = json['athlete']= new Athlete.fromJson(json['athlete']);
    username = json['username'];
    athleteGender = json['athlete_gender'];
    athleteCategoryInCompetition = json['athlete_category_in_competition'];
    ranking = json['ranking'];
    globalPontuation = json['global_pontuation'];
    qValidated = json['Q_validated'];
    round = json['round'];
    qHeatNumber = json['Q_Heat_number'];
    qStartingList = json['Q_Starting_list'];
    q1stJudgeLastName = json['Q_1st_Judge_Last_name'];
    q1stJudgeFirstName = json['Q_1st_judge_first_name'];
    q1stJudgeIwwfId = json['Q_1st_judge_iwwf_id'];
    q2ndJudgeLastName = json['Q_2nd_Judge_Last_name'];
    q2ndJudgeFirstName = json['Q_2nd_judge_first_name'];
    q2ndJudgeIwwfId = json['Q_2nd_judge_iwwf_id'];
    q3rdJudgeLastName = json['Q_3rd_Judge_Last_name'];
    q3rdJudgeFirstName = json['Q_3rd_judge_first_name'];
    q3rdJudgeIwwfId = json['Q_3rd_judge_iwwf_id'];
    q1stJudgeAtlheteFrontFoot = json['Q_1st_judge_atlhete_front_foot'];
    q2ndJudgeAtlheteFrontFoot = json['Q_2nd_judge_atlhete_front_foot'];
    q3rdJudgeAtlheteFrontFoot = json['Q_3rd_judge_atlhete_front_foot'];
    q1stJudgeIntensityScore = json['Q_1st_judge_Intensity_score'];
    q2ndJudgeIntensityScore = json['Q_2nd_judge_Intensity_score'];
    q3rdJudgeIntensityScore = json['Q_3rd_judge_Intensity_score'];
    q1stJudgeExecutionScore = json['Q_1st_judge_Execution_score'];
    q2ndJudgeExecutionScore = json['Q_2nd_judge_Execution_score'];
    q3rdJudgeExecutionScore = json['Q_3rd_judge_Execution_score'];
    q1stJudgeCompositionScore = json['Q_1st_judge_Composition_score'];
    q2ndJudgeCompositionScore = json['Q_2nd_judge_Composition_score'];
    q3rdJudgeCompositionScore = json['Q_3rd_judge_Composition_score'];
    q1stJudgeGlobalScore = json['Q_1st_judge_global_score'];
    q2ndJudgeGlobalScore = json['Q_2nd_judge_global_score'];
    q3rdJudgeGlobalScore = json['Q_3rd_judge_global_score'];
    q1stJudgeTricksCount = json['Q_1st_judge_tricks_count'];
    q2ndJudgeTricksCount = json['Q_2nd_judge_tricks_count'];
    q3rdJudgeTricksCount = json['Q_3rd_judge_tricks_count'];
    q1stJudgeInvertsCount = json['Q_1st_judge_Inverts_count'];
    q2ndJudgeInvertsCount = json['Q_2nd_judge_Inverts_count'];
    q3rdJudgeInvertsCount = json['Q_3rd_judge_Inverts_count'];
    q1stJudgeRotationsCount = json['Q_1st_judge_Rotations_count'];
    q2ndJudgeRotationsCount = json['Q_2nd_judge_Rotations_count'];
    q3rdJudgeRotationsCount = json['Q_3rd_judge_Rotations_count'];
    q1stJudgeFallsCount = json['Q_1st_judge_Falls_count'];
    q2ndJudgeFallsCount = json['Q_2nd_judge_Falls_count'];
    q3rdJudgeFallsCount = json['Q_3rd_judge_Falls_count'];
    q1stJudgeNotes = json['Q_1st_judge_notes'];
    q2ndJudgeNotes = json['Q_2nd_judge_notes'];
    q3rdJudgeNotes = json['Q_3rd_judge_notes'];

    qGlobalIntensityScore = json['Q_global_Intensity_score'];
    qGlobalExecutionScore = json['Q_global_execution_score'];
    qGlobalCompositionScore = json['Q_global_composition_score'];
    qGlobalScore = json['Q_global_score'];

    qGlobalIntensityPontuation = json['Q_global_Intensity_pontuation'];
    qGlobalExecutionPontuation = json['Q_global_execution_pontuation'];
    qGlobalCompositionPontuation = json['Q_global_composition_pontuation'];
    qGlobalPontuation = json['Q_global_pontuation'];

    qPlacement = json['Q_placement']==null?"":json['Q_placement'];
    competition = json['competition'];


    if(qPlacement ==1){
      placementText= qPlacement.toString()+"st";
    }else if(qPlacement ==2){
      placementText= qPlacement.toString()+"nd";
    } else if(qPlacement ==3){
      placementText= qPlacement.toString()+"rd";
    }else if(qPlacement! > 3){
      placementText= qPlacement.toString()+"th";
    }else{
      placementText="";
    }
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    data['id'] = this.id;
    data['athlete_id'] = this.athlete!.id;
    data['username'] = this.username;
    data['athlete_gender'] = this.athleteGender;
    data['athlete_category_in_competition'] = this.athleteCategoryInCompetition;
    data['ranking'] = this.ranking;
    data['global_pontuation'] = this.globalPontuation;
    data['Q_validated'] = this.qValidated;
    data['round'] = this.round;
    data['Q_Heat_number'] = this.qHeatNumber;
    data['Q_Starting_list'] = this.qStartingList;
    data['Q_1st_Judge_Last_name'] = this.q1stJudgeLastName;
    data['Q_1st_judge_first_name'] = this.q1stJudgeFirstName;
    data['Q_1st_judge_iwwf_id'] = this.q1stJudgeIwwfId;
    data['Q_2nd_Judge_Last_name'] = this.q2ndJudgeLastName;
    data['Q_2nd_judge_first_name'] = this.q2ndJudgeFirstName;
    data['Q_2nd_judge_iwwf_id'] = this.q2ndJudgeIwwfId;
    data['Q_3rd_Judge_Last_name'] = this.q3rdJudgeLastName;
    data['Q_3rd_judge_first_name'] = this.q3rdJudgeFirstName;
    data['Q_3rd_judge_iwwf_id'] = this.q3rdJudgeIwwfId;
    data['Q_1st_judge_atlhete_front_foot'] = this.q1stJudgeAtlheteFrontFoot;
    data['Q_2nd_judge_atlhete_front_foot'] = this.q2ndJudgeAtlheteFrontFoot;
    data['Q_3rd_judge_atlhete_front_foot'] = this.q3rdJudgeAtlheteFrontFoot;
    data['Q_1st_judge_Intensity_score'] = this.q1stJudgeIntensityScore;
    data['Q_2nd_judge_Intensity_score'] = this.q2ndJudgeIntensityScore;
    data['Q_3rd_judge_Intensity_score'] = this.q3rdJudgeIntensityScore;
    data['Q_1st_judge_Execution_score'] = this.q1stJudgeExecutionScore;
    data['Q_2nd_judge_Execution_score'] = this.q2ndJudgeExecutionScore;
    data['Q_3rd_judge_Execution_score'] = this.q3rdJudgeExecutionScore;
    data['Q_1st_judge_Composition_score'] = this.q1stJudgeCompositionScore;
    data['Q_2nd_judge_Composition_score'] = this.q2ndJudgeCompositionScore;
    data['Q_3rd_judge_Composition_score'] = this.q3rdJudgeCompositionScore;
    data['Q_1st_judge_global_score'] = this.q1stJudgeGlobalScore;
    data['Q_2nd_judge_global_score'] = this.q2ndJudgeGlobalScore;
    data['Q_3rd_judge_global_score'] = this.q3rdJudgeGlobalScore;
    data['Q_1st_judge_tricks_count'] = this.q1stJudgeTricksCount;
    data['Q_2nd_judge_tricks_count'] = this.q2ndJudgeTricksCount;
    data['Q_3rd_judge_tricks_count'] = this.q3rdJudgeTricksCount;
    data['Q_1st_judge_Inverts_count'] = this.q1stJudgeInvertsCount;
    data['Q_2nd_judge_Inverts_count'] = this.q2ndJudgeInvertsCount;
    data['Q_3rd_judge_Inverts_count'] = this.q3rdJudgeInvertsCount;
    data['Q_1st_judge_Rotations_count'] = this.q1stJudgeRotationsCount;
    data['Q_2nd_judge_Rotations_count'] = this.q2ndJudgeRotationsCount;
    data['Q_3rd_judge_Rotations_count'] = this.q3rdJudgeRotationsCount;
    data['Q_1st_judge_Falls_count'] = this.q1stJudgeFallsCount;
    data['Q_2nd_judge_Falls_count'] = this.q2ndJudgeFallsCount;
    data['Q_3rd_judge_Falls_count'] = this.q3rdJudgeFallsCount;
    data['Q_1st_judge_notes'] = this.q1stJudgeNotes;
    data['Q_2nd_judge_notes'] = this.q2ndJudgeNotes;
    data['Q_3rd_judge_notes'] = this.q3rdJudgeNotes;
    data['Q_global_Intensity_score'] = this.qGlobalIntensityScore;
    data['Q_global_execution_score'] = this.qGlobalExecutionScore;
    data['Q_global_composition_score'] = this.qGlobalCompositionScore;
    data['Q_global_score'] = this.qGlobalScore;
    data['Q_global_Intensity_pontuation'] = this.qGlobalIntensityPontuation;
    data['Q_global_execution_pontuation'] = this.qGlobalExecutionPontuation;
    data['Q_global_composition_pontuation'] = this.qGlobalCompositionPontuation;
    data['Q_global_pontuation'] = this.qGlobalPontuation;
    data['Q_placement'] = this.qPlacement==null?"":this.qPlacement;
    data['competition'] = this.competition;
    return data;
  }
}

class Athlete {
  int? id;
  String fedId="";
  String firstName="";
  String lastName="";
  String  country="";
  Athlete(
      {this.id,
        required this.fedId,
        required this.firstName,
        required this.lastName,required this.country});

  Athlete.fromJson(Map<String, dynamic> json) {
    id = json['id'];
    fedId = json['fed_id'];
    firstName = json['first_name'];
    lastName = json['last_name'];
    country = json['country'];
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    data['id'] = this.id;
    data['fed_id'] = this.fedId;
    data['first_name'] = this.firstName;
    data['last_name'] = this.lastName;
    data['country'] = this.country;
    return data;
  }
}