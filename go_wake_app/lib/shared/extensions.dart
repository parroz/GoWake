import 'package:flag/flag_enum.dart';

 class Extensions{

  static  FlagsCode getFlagCode(String? organizingCountry) {
    if(organizingCountry?.toLowerCase()=="esp"||organizingCountry?.toLowerCase()=="es")
      return FlagsCode.ES;
    if(organizingCountry?.toLowerCase()=="pt")
      return FlagsCode.PT;
    if(organizingCountry?.toLowerCase()=="fr")
      return FlagsCode.FR;
    if(organizingCountry?.toLowerCase()=="us"||organizingCountry?.toLowerCase()=="usa"||organizingCountry?.toLowerCase()=="eua")
      return FlagsCode.US;
    if(organizingCountry?.toLowerCase()=="ua")
      return FlagsCode.UA;
    if(organizingCountry?.toLowerCase()=="br" ||organizingCountry?.toLowerCase()=="brz")
      return FlagsCode.BR;


    return FlagsCode.PT;
  }
}