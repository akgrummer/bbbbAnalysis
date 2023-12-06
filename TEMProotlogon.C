#include "AidanStyle/AidanStyle.C"
void rootlogon()
{
  // Load Aidan style
  //gROOT->LoadMacro("AidanStyle.C"); //No longer works for ROOT6
  SetAidanStyle();
}
