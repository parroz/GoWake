import 'dart:ffi';

class CompetitionDetail {
  int? id;
  List<Category> _categories = [];
  List<Category> get categories => _categories;
  String _code = "";
  String get code => _code;
  String _discipline = "";
  String get discipline => _discipline;
  String _name = "";
  String get name => _name;
  String _organizingCountry = "";
  String get organizingCountry => _organizingCountry;
  String _tournamentType = "";
  String get tournamentType => _tournamentType;
  String _venue = "";
  String get venue => _venue;
  String _siteCode = "";
  String get siteCode => _siteCode;
  String _ageGroups = "";
  String get ageGroups => _ageGroups;
  DateTime _beginningDate= DateTime.now();
  DateTime get beginningDate => _beginningDate;
  DateTime _endDate= DateTime.now();
  DateTime get endDate => _endDate;

  CompetitionDetail();

  CompetitionDetail.fromJson(Map<String, dynamic> json) {
    id = json['id'];
    if (json['leaderboards'] != null) {
      _categories = [];
      json['leaderboards'].forEach((v) {
        categories.add(new Category.fromJson(v));
      });
    }

    _code = json['code'];
    _discipline = json['discipline'];
    _name = json['name'];
    _organizingCountry = json['organizing_country'];
    _tournamentType = json['tournament_type'];
    _venue = json['venue'];
    _siteCode = json['site_code'];
    _ageGroups = json['age_groups'];
    _beginningDate = DateTime.parse(json['beginning_date'].toString())   ;
    _endDate = DateTime.parse(json['end_date'].toString())   ;
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    data['id'] = this.id;
    if (this.categories != null) {
      data['leaderboards'] =
          this.categories.map((v) => v.toJson()).toList();
    }

    data['code'] = this.code;
    data['discipline'] = this.discipline;
    data['name'] = this.name;
    data['organizing_country'] = this.organizingCountry;
    data['tournament_type'] = this.tournamentType;
    data['venue'] = this.venue;
    data['site_code'] = this.siteCode;
    data['age_groups'] = this.ageGroups;
    data['beginning_date'] = this.beginningDate;
    data['end_date'] = this.endDate;
    return data;
  }
}

class Category {
  String? athleteCategoryInCompetition;
  String? athleteGender;
  String? round;
  String? q_heat_number;
  bool expanded= false;
  Category(
      {
        this.athleteCategoryInCompetition,
        this.athleteGender,this.round,this.q_heat_number});

  Category.fromJson(Map<String, dynamic> json) {
    athleteCategoryInCompetition = json['athlete_category_in_competition'];
    athleteGender = json['athlete_gender'];
    round = json['round'];
    q_heat_number = json['Q_Heat_number'];
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    data['athlete_category_in_competition'] = this.athleteCategoryInCompetition;
    data['athlete_gender'] = this.athleteGender;
    data['round'] = this.round;
    data['Q_Heat_number'] = this.q_heat_number;
    return data;
  }
}