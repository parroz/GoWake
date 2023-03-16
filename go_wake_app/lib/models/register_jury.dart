class RegisterJury {
  String _response="";
  String get response => _response;
  String _username="";
  String get username => _username;
  String _email="";
  String get email => _email;
  String _token="";
  String get token => _token;
  String _error="";
  String get error => _error;


  RegisterJury.fromJson(Map<String, dynamic> json) {
    if (json.containsKey('error')) {
      _error = json['error'];
    }else{
      _response = json['response'];
      _username = json['username'];
      _email = json['email'];
      _token = json['token'];
    }
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    data['response'] = this.response;
    data['username'] = this.username;
    data['email'] = this.email;
    data['token'] = this.token;
    return data;
  }
}