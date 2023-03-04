import 'package:flutter/cupertino.dart';

import '../../models/auth.dart';
import '../../services/services.dart';

enum LoginState { WAITING, LOADING, SUCCESS, FAIL }

class LoginController extends ChangeNotifier  {
  LoginState _state = LoginState.WAITING;
  LoginState get state => _state;

  final usernameController = TextEditingController();
  final passwordController = TextEditingController();

  Future<void> login() async {
    _state = LoginState.LOADING;
    notifyListeners();
    try {
      final Services service = Services ();
      Auth response = await service.authentication(usernameController.text,passwordController.text);
      _state = LoginState.SUCCESS;
      notifyListeners();
      } catch (error) {
      _state = LoginState.FAIL;
      notifyListeners();
      }

  }
}