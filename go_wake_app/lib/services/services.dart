import 'dart:convert';

import 'package:go_wake_app/services/service_locator.dart';

import '../api/api_service.dart';
import '../models/auth.dart';
import '../models/register_jury.dart';
import '../storage/secure_storage_service .dart';


class Services{
  Future<Auth> authentication(String username,String password) async{
    final ApiService apiService = ApiService();
    final response = await  apiService.login(username, password);

    if (response.statusCode == 200) {
      Auth auth = Auth.fromJson(jsonDecode(response.body));
      final SecureStorageService _secureStorageService =
      serviceLocator<SecureStorageService>();
      _secureStorageService.writeToken(auth.token);
      String credentials = "${auth.username};${auth.email};${auth.role};$password";
      _secureStorageService.writeCredentials(credentials);
    }

    return Auth.fromJson(jsonDecode(response.body));
  }

  Future<RegisterJury> register(String username, String password, String password2, String email,String code) async {
    final ApiService apiService = ApiService();
    final response = await  apiService.register(username, password,password2,email,code);
    if (response.statusCode == 201) {
      RegisterJury registerJury = RegisterJury.fromJson(jsonDecode(response.body));
      final SecureStorageService _secureStorageService =
      serviceLocator<SecureStorageService>();
      _secureStorageService.writeToken(registerJury.token);
      String credentials = "$username;$email;${"Jury"};$password";
      _secureStorageService.writeCredentials(credentials);
    }
    return RegisterJury.fromJson(jsonDecode(response.body));
  }

}