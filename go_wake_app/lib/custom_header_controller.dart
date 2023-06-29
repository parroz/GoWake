import 'package:flutter/cupertino.dart';

import '../../services/service_locator.dart';
import '../../storage/secure_storage_service .dart';

class HeaderController extends ChangeNotifier  {
  String username ="";
  String email ="";

  void getCredentials() async {
    final SecureStorageService _secureStorageService =
    serviceLocator<SecureStorageService>();
    final credentials = await _secureStorageService.getCredentials();
    if (credentials != null) {
      var wfield = credentials.split(";");
      username = wfield[0];
      email = wfield[1];
    }
    notifyListeners();
  }
}