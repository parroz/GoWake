import 'package:flutter/cupertino.dart';
import 'package:go_wake_app/shared/constants.dart';

import '../../services/service_locator.dart';
import '../../storage/secure_storage_service .dart';

class NavigationDrawerController extends ChangeNotifier  {
  LoginState _state = LoginState.WAITING;
  LoginState get state => _state;

  Future<void> signOut() async {
    _state = LoginState.LOADING;
    notifyListeners();
    try {
      final SecureStorageService _secureStorageService =
      serviceLocator<SecureStorageService>();
      _secureStorageService.deleteToken();
      _state = LoginState.SUCCESS;
      notifyListeners();
      _state = LoginState.WAITING;
      notifyListeners();
    } catch (error) {
      _state = LoginState.FAIL;
      notifyListeners();
    }
  }
}