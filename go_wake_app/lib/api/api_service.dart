import 'package:go_wake_app/models/competition_detail.dart';
import 'package:go_wake_app/models/judge_leaderboard.dart';
import 'package:http/http.dart';
import 'package:http/http.dart' as http;

import '../services/service_locator.dart';
import '../shared/constants.dart';
import '../storage/secure_storage_service .dart';
import 'dart:convert';
class ApiService {
  final SecureStorageService _secureStorageService =
      serviceLocator<SecureStorageService>();

  ApiService();

  Future<Response>  updateJudgeSheet(LeaderboardJudge leaderboard, String id, String competition ) async {
    final String jsonString = jsonEncode(leaderboard);
    return await http.put(
       Uri.parse('${Constants.URL_API}/api/competition/$competition/leaderboard/$id/'),
           headers: await getRequestHeaders(),
           body: jsonString );
  }
  Future<Response> login(String username, String password) async {
    return await http.post(Uri.parse('${Constants.URL_API}/account/login-app/'),
        body: {'username': username, 'password': password});
  }

  Future<Response> register(String username, String password, String password2,
      String email, String code) async {
    return await http
        .post(Uri.parse('${Constants.URL_API}/account/register-jury/'), body: {
      'username': username,
      'email': email,
      'group': 'jury',
      'password': password,
      'password2': password2,
      'code': code
    });
  }

  Future<Map<String, String>> getRequestHeaders() async {
    final accessToken = await _secureStorageService.getToken();
    final headers = {'Authorization': 'Token $accessToken',
      'Content-Type': 'application/json'};
    return headers;
  }

  Future<Response> getCompetitions() async {
    final iwwfId = await _secureStorageService.getIwwfId();
    return await http.get(
        Uri.parse('${Constants.URL_API}/api/competitions-calendar/$iwwfId'),
        headers: await getRequestHeaders());
  }

  Future<Response> getCompetitionDetail(String id) async {
    return await http.get(
        Uri.parse('${Constants.URL_API}/api/competition-app-detail/$id'),
        headers: await getRequestHeaders());
  }
  Future<Response> getLeaderboardsByCategory(Category item, int? id) async {
    return await http.get(
        Uri.parse('${Constants.URL_API}/api/competition/$id/category/${item.athleteCategoryInCompetition}/gender/${item.athleteGender}/round/${item.round}/heat/${item.q_heat_number}/'),
        headers: await getRequestHeaders());
  }
  Future<Response> getLeaderboard( String id) async {
    return await http.get(
        Uri.parse('${Constants.URL_API}/api/leaderboard/$id/'),
        headers: await getRequestHeaders());
  }



}
