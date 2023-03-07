
import 'package:http/http.dart';
import 'package:http/http.dart' as http;

import '../shared/constants.dart';
class ApiService {

  ApiService();
  //final _urlLogin = 'https://gowake.daletech.pt/api';

  Future<Response> getAllCountries() async {
    String url =  'https://api.apilayer.com/fixer/symbols';
    return await http.get(
      Uri.parse(
          url),
      headers: getRequestHeaders(),
    );
  }
  Future<Response> login(String username,String password) async {
    //password="iVSK7X!ynP09";
    return await http.post(Uri.parse('${Constants.URL_API}/account/login/'), body: {'username': username, 'password': password});
  }
  Future<Response> register(String username, String password, String password2, String email, String code)async {
    return await http.post(Uri.parse('${Constants.URL_API}/account/register-jury/'),
        body: {'username': username,'email':email,'group':'jury', 'password': password, 'password2': password2,'code': code});
  }
  getRequestHeaders() {
    final headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    };
    return headers;
  }

  Future<Response> latestCurrency(String base) async{
    String url =  'https://api.apilayer.com/fixer/latest?symbols=EUR%2CUSD%2CBRL%2CBTC%2CCNY%2CRUB%2CGBP%2CCHF%2CJPY&base='+base;
    return await http.get(
      Uri.parse(
          url),
      headers: getRequestHeaders(),
    );
  }




}