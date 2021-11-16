<?php

namespace JutiaDev\Category\Traits;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphToMany;
use JutiaDev\Category\Models\Categorizable;
use JutiaDev\Category\Models\Category;

trait HasCategories
{
    public static function bootHasCategories()
    {
        static::deleting(function ($model) {
            if (method_exists($model, 'isForceDeleting') && !$model->isForceDeleting()) {
                return;
            }

            Categorizable::where(Categorizable::CATEGORIZABLE_ID, $model->{$model->getKeyName()})
                ->where(Categorizable::CATEGORIZABLE_TYPE, get_class($model))
                ->delete();
        });
    }

    public function categories(): MorphToMany
    {
        /** @var Model $this */
        return $this->morphToMany(Category::class, 'categorizable');
    }

    public function getRelationshipName(): ?string
    {
        return $this->relationshipName ?? null;
    }

}
