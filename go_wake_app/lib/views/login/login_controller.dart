import 'package:flutter/cupertino.dart';

import '../../models/auth.dart';
import '../../services/services.dart';
import '../../shared/constants.dart';

//enum LoginState { WAITING, LOADING, SUCCESS, FAIL }

class LoginController extends ChangeNotifier  {
  LoginState _state = LoginState.WAITING;
  LoginState get state => _state;
  String _errorMsg = "";
  String get errorMsg => _errorMsg;
  final usernameController = TextEditingController();
  final passwordController = TextEditingController();

  Future<void> login() async {
    _state = LoginState.LOADING;
    notifyListeners();
    try {
      final Services service = Services ();
      Auth auth = await service.authentication(usernameController.text,passwordController.text);
      if(auth.error.isEmpty){
        _state = LoginState.SUCCESS;
      }else{
        _state = LoginState.FAIL;
        _errorMsg = auth.error;
      }
      notifyListeners();
      } catch (error) {
      _errorMsg = error.toString();
      _state = LoginState.FAIL;
      notifyListeners();
      }

  }
}