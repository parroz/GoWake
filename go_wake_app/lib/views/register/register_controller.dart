import 'package:flutter/cupertino.dart';

import '../../models/auth.dart';
import '../../models/register_jury.dart';
import '../../services/services.dart';
import '../../shared/constants.dart';

class RegisterController extends ChangeNotifier  {
  LoginState _state = LoginState.WAITING;
  LoginState get state => _state;
  String _errorMsg = "";
  String get errorMsg => _errorMsg;
  final usernameController = TextEditingController();
  final emailController = TextEditingController();
  final codeController = TextEditingController();
  final passwordController = TextEditingController();
  final password2Controller = TextEditingController();

  Future<void> register() async {
    _state = LoginState.LOADING;
    notifyListeners();
    try {
      final Services service = Services ();
      RegisterJury auth = await service.register(usernameController.text,
          passwordController.text,password2Controller.text,emailController.text,codeController.text);
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