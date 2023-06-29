import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

class ConfigurationController extends ChangeNotifier  {
  final themeMode = ValueNotifier(ThemeMode.system);

  void changeThemeMode(ThemeMode? mode) {
    if (mode != null) {
      themeMode.value = mode;
      notifyListeners();
    }
  }

}