include "MapEnums"
include "MapUtilities"
include "MountainsCliffs"
include "RiversLakes"
include "FeatureGenerator"
include "TerrainGenerator"
include "NaturalWonderGenerator"
include "ResourceGenerator"
include "AssignStartingPlots"

local g_iW = [Length]
local g_iH = [Height]
local g_iFlags = {}
local g_continentsFrac = nil

function GetMapInitData(worldSize)
	return {
		Width = g_iW,
		Height = g_iH,
		WrapX = false,
		WrapY = false,
	};
end

function GetNaturalWonders()
	local NaturalWonders = {}

	return NaturalWonders
end

function GenerateMap()
	print("Calling Map Generator");
	GenerateImportedMap(GetMap(), GetCiv6DataToConvert(), GetNaturalWonders(), g_iW, g_iH);
end

function GetCiv6DataToConvert()
	return {}
end

function GetMap()
	local MapToConvert = {}
	for i = 0, g_iW - 1, 1 do
		MapToConvert[i] = {}
	end
