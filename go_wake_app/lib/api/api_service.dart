import 'package:http/http.dart';
import 'package:http/http.dart' as http;

import '../services/service_locator.dart';
import '../shared/constants.dart';
import '../storage/secure_storage_service .dart';

class ApiService {
  final SecureStorageService _secureStorageService =
      serviceLocator<SecureStorageService>();

  ApiService();

  Future<Response> login(String username, String password) async {
    return await http.post(Uri.parse('${Constants.URL_API}/account/login/'),
        body: {'username': username, 'password': password});
  }

  Future<Response> register(String username, String password, String password2,
      String email, String code) async {
    return await http
        .post(Uri.parse('${Constants.URL_API}/account/register-jury/'), body: {
      'username': username,
      'email': email,
      'group': 'jury',
      'password': password,
      'password2': password2,
      'code': code
    });
  }

  Future<Map<String, String>> getRequestHeaders() async {
    final accessToken = await _secureStorageService.getToken();
    final headers = {'Authorization': 'Token $accessToken'};
    return headers;
  }

  Future<Response> getCompetitions() async {
    return await http.get(
        Uri.parse('${Constants.URL_API}/api/competitions-calendar/'),
        headers: await getRequestHeaders());
  }
}
