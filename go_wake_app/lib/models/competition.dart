class ResultCompetition {
  int _count = 0;
  int get count => _count;
  String _next = "";
  String get next => _next;
  String _previous = "";
  String get previous => _previous;
  List<Competition> get competitions => _results;
  List<Competition> _results = [];
  ResultCompetition();

  ResultCompetition.fromJson(Map<String, dynamic> json) {
    _count = json['count'];
    if (json['next'] != null) {
      _next = json['next'];
    }
    if (json['previous'] != null) {
      _previous = json['previous'];
    }

    if (json['results'] != null) {
      _results = <Competition>[];
      json['results'].forEach((v) {
        _results.add(Competition.fromJson(v));
      });
    }
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    data['count'] = this.count;
    data['next'] = this.next;
    data['previous'] = this.previous;
    if (this.competitions != null) {
      data['results'] = this.competitions.map((v) => v.toJson()).toList();
    }
    return data;
  }
}

class Competition {
  int? id;
  String? username;
  String? code;
  String? discipline;
  String? name;
  String? organizingCountry;
  String? tournamentType;
  String? venue;
  String? siteCode;
  String? ageGroups;
  DateTime? beginningDate;
  DateTime? endDate;

  Competition(
      {this.id,
      this.username,
      this.code,
      this.discipline,
      this.name,
      this.organizingCountry,
      this.tournamentType,
      this.venue,
      this.siteCode,
      this.ageGroups,
      this.beginningDate,
      this.endDate});

  Competition.fromJson(Map<String, dynamic> json) {
    id = json['id'];
    username = json['username'];
    code = json['code'];
    discipline = json['discipline'];
    name = json['name'];
    organizingCountry = json['organizing_country'];
    tournamentType = json['tournament_type'];
    venue = json['venue'];
    siteCode = json['site_code'];
    ageGroups = json['age_groups'];
    beginningDate = DateTime.parse(json['beginning_date'].toString())   ;
    endDate = DateTime.parse(json['end_date'].toString())   ;
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    data['id'] = this.id;
    data['username'] = this.username;
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
