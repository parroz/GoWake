import 'package:get_it/get_it.dart';

import '../api/api_service.dart';
import '../storage/secure_storage_service .dart';


GetIt serviceLocator = GetIt.instance;


void setupServiceLocator({bool testing = false }) {

  serviceLocator.registerLazySingleton<SecureStorageService >(() => SecureStorageService ());
  serviceLocator.registerLazySingleton<ApiService>(() => ApiService());

}