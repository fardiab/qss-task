import graphene
from graphene_django import DjangoObjectType
from graphene_django import DjangoListField
from core.models import Country, Indica, Sect, SubSect


class CountryType(DjangoObjectType):
    indicator = graphene.String()
    country = graphene.String()
    rank = graphene.String()
    amount = graphene.String()
    year = graphene.String()

    class Meta:
        model = Country
        fields = ("id",)


class IndicaType(DjangoObjectType):
    subsector = graphene.String()

    class Meta:
        model = Indica
        fields = ("id", "indicator")


class SubSectType(DjangoObjectType):
    sector = graphene.String()

    class Meta:
        model = SubSect
        fields = ("id", "subsector")


class SectType(DjangoObjectType):
    subsector = graphene.Field(SubSectType)

    class Meta:
        model = Sect
        fields = ("id", "sector", "subsector")

    def resolve_subsector(self, info):
        return self.subsect_set.all()


class Query(graphene.ObjectType):
    countries = graphene.Field(CountryType, id=graphene.Int())
    indicators = graphene.Field(IndicaType, id=graphene.Int())
    subsectors = graphene.Field(SubSectType, id=graphene.Int())
    sectors = graphene.Field(SectType, id=graphene.Int())

    def resolve_countries(self, info, id):
        return Country.objects.get(pk=id)

    def resolve_indicators(self, info, id):
        return Indica.objects.get(pk=id)

    def resolve_subsectors(self, info, id):
        return SubSect.objects.get(pk=id)

    def resolve_sectors(self, info, id):
        return Sect.objects.get(pk=id)


schema = graphene.Schema(query=Query)
