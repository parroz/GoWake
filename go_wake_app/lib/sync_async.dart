import 'package:http/http.dart' as http;
void main(){
  fetch();
}

Future fetch() async {
  var url ='https://gowake.daletech.pt/api/competitions/';
  var token ='59a1cebcaf74bc4f085b5cc4688a301270c4897d';
  var response = await http.get(Uri.parse(url),headers: {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'Token $token',
  });
  print(response.body);

  var urlLogin = 'https://gowake.daletech.pt/api/auth/';
  var responseLogin = await http.post(Uri.parse(urlLogin), body: {'username': 'admin', 'password': 'iVSK7X!ynP09'});
  print('Response status: ${responseLogin.statusCode}');
  print('Response body: ${responseLogin.body}');
}