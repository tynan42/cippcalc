from wtforms import Form, TextField, FloatField, validators
import math

class ErrorValidation(Form):
    design_condition = TextField('Design Condition', [
                        validators.Required(message='Required field')])
    location = TextField('Location', [
                        validators.Required(message='Required field')])
    host_diameter = FloatField('Host Pipe Diameter', [
                        validators.NumberRange(min=4, max=96, message='Host Pipe Diameter out of range')])
    surface_to_invert = FloatField('Depth to Invert', [
                        validators.NumberRange(min=0, max=50, message='Must be a number between 0 and 50')])
    gw_level = FloatField('Groundwater Depth', [
                        validators.NumberRange(min=0, max=100, message='Must be a number between 0 and 100'),
                        validators.Optional()])
    design_modulus = FloatField('Design Elastic Modulus', [
                        validators.NumberRange(min=1, max=None, message='Value must be a positive integer'),
                        validators.Optional()])
    design_flexural_strength = FloatField('Design Flexural Strength', [
                        validators.NumberRange(min=1, max=None, message='''Design flexural strength out \
                        of normal range.'''),
                        validators.Optional()])
    safety_factor = FloatField('Safety Factor', [
                        validators.NumberRange(min=0.1, max=100, message='Safety Factor out of range'),
                        validators.Optional()])
    ret_factor = FloatField('Long Term Retention Factor', [
                        validators.NumberRange(min=1, max=100, message='Retention out of range'),
                        validators.Optional()])
    ovality = FloatField('Ovality', [
                        validators.NumberRange(min=0, max=100, message='Ovality out of range'),
                        validators.Optional()])
    enhancement_factor = FloatField('Enhancement Factor', [
                        validators.NumberRange(min=1, max=100, message='Enhancement Factor out of range'),
                        validators.Optional()])
    soil_density = FloatField('Soil Density', [
                        validators.NumberRange(min=1, max=1000, message='Soil density out of range'),
                        validators.Optional()])
    poissons = FloatField('Poisson\'s Ratio', [
                        validators.NumberRange(min=0, max=0.5, message='Poisson\'s Ratio out of range'),
                        validators.Optional()])
    soil_mod = FloatField('Modulus of Soil Reaction', [
                        validators.NumberRange(min=200, max=3500, message='Soil Modulus out of range'),
                        validators.Optional()])
    n_host = FloatField('Host Manning\'s', [
                        validators.NumberRange(min=0.005, max=0.20, message='Host Manning\'s out of range'),
                        validators.Optional()])
    n_liner = FloatField('Liner Manning\'s', [
                        validators.NumberRange(min=0.005, max=0.20, message='Liner Manning\'s out of range'),
                        validators.Optional()])
    host_age = FloatField('Host Pipe Age', [
                        validators.NumberRange(min=0, message='Host Pipe Age out of range'),
                        validators.Optional()])
class WarningValidation(Form):
    design_modulus = FloatField('Design Elastic Modulus', [
                        validators.NumberRange(min=250000, max=750000, message='''Design elastic modulus \
                        out of normal range. ASTM minimum value is 250,000 psi.'''),
                        validators.Optional()])
    design_flexural_strength = FloatField('Design Flexural Strength', [
                        validators.NumberRange(min=4500, max=25000, message='''Design flexural strength out \
                        of normal range. ASTM minimum value is 4,500 psi.'''),
                        validators.Optional()])
    ovality = FloatField('Ovality', [
                        validators.NumberRange(min=0, max=30, message='''Ovality indicates pipe may be \
                        partially collapsed. Verify that host pipe is a canditate for CIPP lining.'''),
                        validators.Optional()])
    enhancement_factor = FloatField('Enhancement Factor', [
                        validators.NumberRange(min=7, message='''ASTM recommends a minimum enhancement \
                        factor of 7.0'''),
                        validators.Optional()])
    soil_density = FloatField('Soil Density', [
                        validators.NumberRange(min=100, max=200, message='''Soil density beyond normal \
                        values. Ensure that the host pipe exists in Earth.'''),
                        validators.Optional()])
    soil_mod = FloatField('Modulus of Soil Reaction', [
                        validators.NumberRange(min=700, max=1500, message='''Soil Modulus out of normal \
                        range'''),
                        validators.Optional()])                   