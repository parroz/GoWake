import 'package:flutter/cupertino.dart';

enum LoginState { WAITING, LOADING, SUCCESS, FAIL }
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

}