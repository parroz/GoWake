import 'package:http/http.dart';
import 'package:http/http.dart' as http;
class ApiService {

  ApiService();
  //final _urlLogin = 'https://gowake.daletech.pt/api';
  final _urlLogin = 'http://10.0.2.2:8000';
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
    password ="mehkol2507";
    return await http.post(Uri.parse('$_urlLogin/account/login/'), body: {'username': username, 'password': password});
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