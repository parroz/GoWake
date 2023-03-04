import 'dart:convert';

import 'package:go_wake_app/services/service_locator.dart';

import '../api/api_service.dart';
import '../models/auth.dart';
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
      _secureStorageService.writeCredentials(password);
    }
    if (response.statusCode == 400) {

    }
    return Auth.fromJson(jsonDecode(response.body));
  }

}